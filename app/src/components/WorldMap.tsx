import { useState, useMemo } from 'react';
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
  Marker
} from 'react-simple-maps';
import { scaleLinear } from 'd3-scale';
import type { Country } from '@/types';

const geoUrl = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

interface WorldMapProps {
  countries: Country[];
  selectedCountry: Country | null;
  onCountrySelect: (country: Country) => void;
}

// Country ISO codes to map to geography IDs
const countryCodeMap: Record<string, string> = {
  'US': 'USA',
  'CN': 'CHN',
  'DE': 'DEU',
  'BR': 'BRA',
  'IN': 'IND',
  'RU': 'RUS',
  'JP': 'JPN',
  'SA': 'SAU',
  'VN': 'VNM',
  'MX': 'MEX',
  'TH': 'THA',
  'TW': 'TWN',
  'KR': 'KOR',
  'GB': 'GBR',
  'FR': 'FRA',
  'CA': 'CAN',
  'AU': 'AUS',
  'SG': 'SGP',
  'AE': 'ARE',
  'ID': 'IDN',
  'ZA': 'ZAF',
  'IT': 'ITA',
  'ES': 'ESP',
  'NL': 'NLD',
  'AR': 'ARG',
  'TR': 'TUR',
  'MY': 'MYS'
};

// Reverse mapping
const reverseCountryCodeMap: Record<string, string> =
  Object.fromEntries(Object.entries(countryCodeMap).map(([k, v]) => [v, k]));

const riskColorScale = scaleLinear<string>()
  .domain([0, 50, 70, 100])
  .range(['#22c55e', '#eab308', '#f97316', '#ef4444']);

interface GeographyType {
  rsmKey: string;
  id: string;
  properties: {
    name: string;
  };
}

export function WorldMap({ countries, selectedCountry, onCountrySelect }: WorldMapProps) {
  const [tooltip, setTooltip] = useState<{ content: string; x: number; y: number } | null>(null);

  const countryMap = useMemo(() => {
    return new Map(countries.map(c => [c.id, c]));
  }, [countries]);

  const getCountryRisk = (geoId: string): Country | undefined => {
    const code = reverseCountryCodeMap[geoId];
    return code ? countryMap.get(code) : undefined;
  };

  const getFillColor = (geoId: string) => {
    const country = getCountryRisk(geoId);
    if (!country) return '#1e293b'; // Default dark gray
    return riskColorScale(country.risk_score);
  };

  const isSelected = (geoId: string) => {
    if (!selectedCountry) return false;
    return countryCodeMap[selectedCountry.id] === geoId;
  };

  const handleMouseEnter = (geo: GeographyType, event: React.MouseEvent) => {
    const country = getCountryRisk(geo.id);
    if (country) {
      setTooltip({
        content: `${country.name} - Risk: ${country.risk_score}`,
        x: event.clientX + 10,
        y: event.clientY - 30
      });
    }
  };

  const handleMouseLeave = () => {
    setTooltip(null);
  };

  const handleClick = (geo: GeographyType) => {
    const country = getCountryRisk(geo.id);
    if (country) {
      onCountrySelect(country);
    }
  };

  return (
    <div className="relative w-full h-full">
      <ComposableMap
        projection="geoMercator"
        projectionConfig={{
          scale: 140,
          center: [0, 25]
        }}
        className="w-full h-full"
        style={{
          background: 'transparent'
        }}
      >
        <ZoomableGroup zoom={1} minZoom={1} maxZoom={4} center={[0, 25]}>
          <Geographies geography={geoUrl}>
            {({ geographies }: { geographies: GeographyType[] }) =>
              geographies.map((geo) => {
                const country = getCountryRisk(geo.id);
                const selected = isSelected(geo.id);

                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill={getFillColor(geo.id)}
                    stroke={selected ? '#3b82f6' : '#334155'}
                    strokeWidth={selected ? 2 : 0.5}
                    style={{
                      default: {
                        fill: getFillColor(geo.id),
                        outline: 'none',
                        transition: 'all 0.3s ease',
                      },
                      hover: {
                        fill: country ? '#60a5fa' : getFillColor(geo.id),
                        outline: 'none',
                        cursor: country ? 'pointer' : 'default',
                      },
                      pressed: {
                        fill: country ? '#3b82f6' : getFillColor(geo.id),
                        outline: 'none',
                      },
                    }}
                    onMouseEnter={(e) => handleMouseEnter(geo, e)}
                    onMouseLeave={handleMouseLeave}
                    onClick={() => handleClick(geo)}
                  />
                );
              })
            }
          </Geographies>

          {/* Markers for countries */}
          {countries.map((country) => (
            <Marker
              key={country.id}
              coordinates={[country.coordinates.lng, country.coordinates.lat]}
            >
              <circle
                r={selectedCountry?.id === country.id ? 8 : 5}
                fill={selectedCountry?.id === country.id ? '#3b82f6' : riskColorScale(country.risk_score)}
                stroke="#0f172a"
                strokeWidth={2}
                className="cursor-pointer transition-all duration-300"
                style={{
                  filter: selectedCountry?.id === country.id
                    ? 'drop-shadow(0 0 8px #3b82f6)'
                    : 'drop-shadow(0 0 4px rgba(0,0,0,0.5))',
                }}
                onClick={() => onCountrySelect(country)}
                onMouseEnter={(e: React.MouseEvent) => {
                  setTooltip({
                    content: `${country.name} - Risk: ${country.risk_score}`,
                    x: e.clientX + 10,
                    y: e.clientY - 30
                  });
                }}
                onMouseLeave={() => setTooltip(null)}
              />
              {selectedCountry?.id === country.id && (
                <circle
                  r={12}
                  fill="none"
                  stroke="#3b82f6"
                  strokeWidth={1}
                  opacity={0.5}
                  className="animate-ping"
                />
              )}
            </Marker>
          ))}
        </ZoomableGroup>
      </ComposableMap>

      {/* Tooltip */}
      {tooltip && (
        <div
          className="fixed z-50 px-3 py-2 text-sm bg-slate-900 border border-slate-700 rounded-lg shadow-xl pointer-events-none"
          style={{
            left: tooltip.x,
            top: tooltip.y,
          }}
        >
          {tooltip.content}
        </div>
      )}

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-sm border border-slate-700 rounded-lg p-4">
        <h4 className="text-sm font-semibold text-slate-300 mb-2">Risk Level</h4>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#22c55e' }} />
            <span className="text-xs text-slate-400">Low (0-40)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#eab308' }} />
            <span className="text-xs text-slate-400">Medium (41-70)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#f97316' }} />
            <span className="text-xs text-slate-400">High (71-85)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded" style={{ backgroundColor: '#ef4444' }} />
            <span className="text-xs text-slate-400">Critical (86-100)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
