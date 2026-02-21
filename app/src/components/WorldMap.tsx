import { useState, useMemo, useRef, useCallback, useEffect } from 'react';
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker
} from 'react-simple-maps';
import { scaleLinear } from 'd3-scale';
import { ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import type { Country } from '@/types';

const geoUrl =
  'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

interface WorldMapProps {
  countries: Country[];
  selectedCountry: Country | null;
  onCountrySelect: (country: Country) => void;
}

const countryCodeMap: Record<string, string> = {
  'US': 'USA', 'CN': 'CHN', 'DE': 'DEU', 'BR': 'BRA', 'IN': 'IND',
  'RU': 'RUS', 'JP': 'JPN', 'SA': 'SAU', 'VN': 'VNM', 'MX': 'MEX',
  'TH': 'THA', 'TW': 'TWN', 'KR': 'KOR', 'GB': 'GBR', 'FR': 'FRA',
  'CA': 'CAN', 'AU': 'AUS', 'SG': 'SGP', 'AE': 'ARE', 'ID': 'IDN',
  'ZA': 'ZAF', 'IT': 'ITA', 'ES': 'ESP', 'NL': 'NLD', 'AR': 'ARG',
  'TR': 'TUR', 'MY': 'MYS', 'CH': 'CHE', 'NO': 'NOR', 'SE': 'SWE',
  'PL': 'POL', 'UA': 'UKR', 'BE': 'BEL', 'PT': 'PRT', 'PH': 'PHL',
  'PK': 'PAK', 'BD': 'BGD', 'IL': 'ISR', 'NZ': 'NZL', 'CL': 'CHL',
  'CO': 'COL', 'PE': 'PER', 'NG': 'NGA', 'EG': 'EGY', 'KE': 'KEN',
  'MA': 'MAR', 'FI': 'FIN', 'DK': 'DNK', 'AT': 'AUT', 'GR': 'GRC',
  'CZ': 'CZE', 'RO': 'ROU', 'KZ': 'KAZ', 'LK': 'LKA', 'KH': 'KHM',
  'MN': 'MNG', 'PA': 'PAN', 'CR': 'CRI', 'EC': 'ECU', 'UY': 'URY',
  'GH': 'GHA', 'ET': 'ETH', 'QA': 'QAT', 'KW': 'KWT', 'OM': 'OMN',
  'JO': 'JOR'
};

const reverseCountryCodeMap: Record<string, string> =
  Object.fromEntries(
    Object.entries(countryCodeMap).map(([k, v]) => [v, k])
  );

const riskColorScale = scaleLinear<string>()
  .domain([0, 50, 70, 100])
  .range(['#22c55e', '#eab308', '#f97316', '#ef4444']);

interface GeographyType {
  rsmKey: string;
  id: string;
  properties: { name: string };
}

// ── Constants ────────────────────────────────────────────────────────────────
const MIN_SCALE = 0.5;
const MAX_SCALE = 8;
const ZOOM_FACTOR = 0.12;        // fraction of current scale per scroll tick

export function WorldMap({ countries, selectedCountry, onCountrySelect }: WorldMapProps) {

  // ── Tooltip (React state OK — low frequency) ─────────────────────────────
  const [tooltip, setTooltip] = useState<{ content: string; x: number; y: number } | null>(null);
  const [hoveredGeoId, setHoveredGeoId] = useState<string | null>(null);
  const [isDraggingState, setIsDraggingState] = useState(false); // for cursor CSS only

  // ── Transform stored in refs → mutated directly, NEVER setState per frame ─
  const wrapperRef = useRef<HTMLDivElement>(null);
  const scaleRef = useRef(1);
  const txRef = useRef(0);
  const tyRef = useRef(0);

  // Drag bookkeeping
  const isDragging = useRef(false);
  const pointerStart = useRef({ x: 0, y: 0, tx: 0, ty: 0 });
  const didDrag = useRef(false);    // distinguish click vs drag

  // rAF dedup for wheel
  const rafId = useRef<number | null>(null);
  const pendingScale = useRef(scaleRef.current);
  const pendingTx = useRef(txRef.current);
  const pendingTy = useRef(tyRef.current);

  // ── Apply CSS transform directly — no React re-render ─────────────────────
  const applyTransform = useCallback((s: number, x: number, y: number, animated = false) => {
    if (!wrapperRef.current) return;
    wrapperRef.current.style.transition = animated
      ? 'transform 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
      : 'none';
    wrapperRef.current.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
    scaleRef.current = s;
    txRef.current = x;
    tyRef.current = y;
    pendingScale.current = s;
    pendingTx.current = x;
    pendingTy.current = y;
  }, []);

  // ── Wheel: zoom toward cursor ─────────────────────────────────────────────
  const handleWheel = useCallback((e: WheelEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const container = wrapperRef.current?.parentElement;
    if (!container) return;

    const rect = container.getBoundingClientRect();
    const cursorX = e.clientX - rect.left;
    const cursorY = e.clientY - rect.top;

    // Accumulate into pending refs (not committed yet → no DOM write mid-accumulation)
    const direction = e.deltaY < 0 ? 1 : -1;
    const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE,
      pendingScale.current * (1 + direction * ZOOM_FACTOR)
    ));
    const scaleDelta = newScale / pendingScale.current;

    // Zoom toward cursor: keep the point under the cursor fixed
    pendingTx.current = cursorX - (cursorX - pendingTx.current) * scaleDelta;
    pendingTy.current = cursorY - (cursorY - pendingTy.current) * scaleDelta;
    pendingScale.current = newScale;

    // Flush once per animation frame
    if (!rafId.current) {
      rafId.current = requestAnimationFrame(() => {
        applyTransform(pendingScale.current, pendingTx.current, pendingTy.current);
        rafId.current = null;
      });
    }
  }, [applyTransform]);

  // Attach wheel listener imperatively so we can pass { passive: false }
  const outerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = outerRef.current;
    if (!el) return;
    el.addEventListener('wheel', handleWheel, { passive: false });
    return () => el.removeEventListener('wheel', handleWheel);
  }, [handleWheel]);

  // ── Pointer drag to pan ───────────────────────────────────────────────────
  const handlePointerDown = useCallback((e: React.PointerEvent) => {
    if (e.button !== 0) return;
    isDragging.current = true;
    didDrag.current = false;
    pointerStart.current = {
      x: e.clientX,
      y: e.clientY,
      tx: pendingTx.current,
      ty: pendingTy.current,
    };
    // ⚠️ Do NOT call setPointerCapture — it steals all pointer events from SVG
    //    child elements (markers, geographies) and breaks their onClick handlers.
    setIsDraggingState(true);
  }, []);

  const handlePointerMove = useCallback((e: React.PointerEvent) => {
    if (!isDragging.current) return;
    const dx = e.clientX - pointerStart.current.x;
    const dy = e.clientY - pointerStart.current.y;
    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) didDrag.current = true;
    if (!didDrag.current) return;

    const newTx = pointerStart.current.tx + dx;
    const newTy = pointerStart.current.ty + dy;

    // Direct DOM write — zero React overhead
    if (wrapperRef.current) {
      wrapperRef.current.style.transition = 'none';
      wrapperRef.current.style.transform = `translate(${newTx}px, ${newTy}px) scale(${pendingScale.current})`;
    }
    pendingTx.current = newTx;
    pendingTy.current = newTy;
    setTooltip(null);
  }, []);

  const handlePointerUp = useCallback(() => {
    isDragging.current = false;
    // Sync refs after drag
    txRef.current = pendingTx.current;
    tyRef.current = pendingTy.current;
    setIsDraggingState(false);
  }, []);

  // ── Zoom buttons (animated) ───────────────────────────────────────────────
  const zoomBy = useCallback((factor: number) => {
    const container = wrapperRef.current?.parentElement;
    if (!container) return;
    const { width, height } = container.getBoundingClientRect();
    const cx = width / 2;
    const cy = height / 2;
    const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, pendingScale.current * factor));
    const scaleDelta = newScale / pendingScale.current;
    const newTx = cx - (cx - pendingTx.current) * scaleDelta;
    const newTy = cy - (cy - pendingTy.current) * scaleDelta;
    applyTransform(newScale, newTx, newTy, true);
  }, [applyTransform]);

  const handleReset = useCallback(() => {
    applyTransform(1, 0, 0, true);
  }, [applyTransform]);

  // ── Country data helpers ──────────────────────────────────────────────────
  const countryMap = useMemo(() =>
    new Map(countries.map(c => [c.id, c])), [countries]);

  const getCountryRisk = (geoId: string): Country | undefined => {
    const code = reverseCountryCodeMap[geoId];
    return code ? countryMap.get(code) : undefined;
  };

  const isSelected = (geoId: string) => {
    if (!selectedCountry) return false;
    return countryCodeMap[selectedCountry.id] === geoId;
  };

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div
      ref={outerRef}
      className="relative w-full h-full bg-[#0b1220] overflow-hidden"
      style={{ cursor: isDraggingState ? 'grabbing' : 'grab' }}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
      onPointerLeave={handlePointerUp}
    >
      {/* ── CSS-transformed wrapper: the ONLY thing that moves ── */}
      <div
        ref={wrapperRef}
        style={{
          width: '100%',
          height: '100%',
          transformOrigin: '0 0',
          willChange: 'transform',
        }}
      >
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{ scale: 140, center: [0, 25] }}
          className="w-full h-full"
        >
          <Geographies geography={geoUrl}>
            {({ geographies }: { geographies: GeographyType[] }) =>
              geographies.map((geo) => {
                const selected = isSelected(geo.id);
                const isHovered = hoveredGeoId === geo.id;

                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    stroke={selected ? '#2563eb' : '#1f2a44'}
                    strokeWidth={selected ? 1.8 : 0.6}
                    style={{
                      default: {
                        fill: isHovered ? '#0f1f3d' : '#16233a',
                        outline: 'none',
                        transition: 'fill 0.2s ease',
                        filter: isHovered ? 'brightness(1.2)' : 'none',
                      },
                      hover: { outline: 'none' },
                      pressed: { outline: 'none' },
                    }}
                    onMouseEnter={(e) => {
                      setHoveredGeoId(geo.id);
                      const country = getCountryRisk(geo.id);
                      if (country) {
                        setTooltip({
                          content: `${country.name} — Risk: ${country.risk_score}`,
                          x: e.clientX + 14,
                          y: e.clientY - 36,
                        });
                      }
                    }}
                    onMouseLeave={() => {
                      setHoveredGeoId(null);
                      setTooltip(null);
                    }}
                    onClick={() => {
                      if (didDrag.current) return; // ignore drag-release as click
                      const country = getCountryRisk(geo.id);
                      if (country) onCountrySelect(country);
                    }}
                  />
                );
              })
            }
          </Geographies>

          {countries.map((country) => {
            const markerColor = riskColorScale(country.risk_score);
            const isActive = selectedCountry?.id === country.id;
            return (
              <Marker
                key={country.id}
                coordinates={[country.coordinates.lng, country.coordinates.lat]}
              >
                {/* Radar-ping rings — only rendered for the selected country */}
                {isActive && (
                  <>
                    <circle
                      r={7}
                      fill="none"
                      stroke={markerColor}
                      strokeWidth={2}
                      className="marker-pulse-ring-1"
                      style={{ pointerEvents: 'none' }}
                    />
                    <circle
                      r={7}
                      fill="none"
                      stroke={markerColor}
                      strokeWidth={1.5}
                      className="marker-pulse-ring-2"
                      style={{ pointerEvents: 'none', opacity: 0.6 }}
                    />
                  </>
                )}

                {/* Main dot */}
                <circle
                  r={isActive ? 7 : 5}
                  fill={markerColor}
                  stroke="#0b1220"
                  strokeWidth={2}
                  style={{
                    transition: 'r 0.2s ease',
                    filter: isActive
                      ? `drop-shadow(0 0 14px ${markerColor})`
                      : `drop-shadow(0 0 6px ${markerColor})`,
                  }}
                  className="cursor-pointer"
                  onClick={(e) => {
                    e.stopPropagation();
                    if (didDrag.current) return;
                    onCountrySelect(country);
                  }}
                  onMouseEnter={(e) => {
                    setTooltip({
                      content: `${country.name} — Risk: ${country.risk_score}`,
                      x: e.clientX + 14,
                      y: e.clientY - 36,
                    });
                  }}
                  onMouseLeave={() => setTooltip(null)}
                />
              </Marker>
            );
          })}
        </ComposableMap>
      </div>

      {/* ── Zoom buttons ───────────────────────────────────────── */}
      <div className="absolute bottom-4 right-4 flex flex-col gap-1.5 z-20">
        <button
          onClick={() => zoomBy(1.5)}
          className="w-8 h-8 flex items-center justify-center bg-slate-800/90 hover:bg-slate-700 border border-slate-600 rounded-lg text-slate-300 hover:text-white transition-all shadow-lg backdrop-blur-sm"
          title="Zoom In"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={() => zoomBy(1 / 1.5)}
          className="w-8 h-8 flex items-center justify-center bg-slate-800/90 hover:bg-slate-700 border border-slate-600 rounded-lg text-slate-300 hover:text-white transition-all shadow-lg backdrop-blur-sm"
          title="Zoom Out"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={handleReset}
          className="w-8 h-8 flex items-center justify-center bg-slate-800/90 hover:bg-slate-700 border border-slate-600 rounded-lg text-slate-300 hover:text-white transition-all shadow-lg backdrop-blur-sm"
          title="Reset View"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* ── Hint ───────────────────────────────────────────────── */}
      <div className="absolute bottom-4 left-3 z-20 pointer-events-none">
        <p className="text-[10px] text-slate-600">Scroll to zoom · Drag to pan</p>
      </div>

      {/* ── Tooltip ────────────────────────────────────────────── */}
      {tooltip && (
        <div
          className="fixed z-50 px-3 py-1.5 text-sm bg-[#111827]/95 border border-slate-700 rounded-lg shadow-xl pointer-events-none text-slate-200 backdrop-blur-md"
          style={{ left: tooltip.x, top: tooltip.y }}
        >
          {tooltip.content}
        </div>
      )}
    </div>
  );
}