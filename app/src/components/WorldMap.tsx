import { useState, useMemo } from 'react';
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker
} from 'react-simple-maps';
import { scaleLinear } from 'd3-scale';
import type { Country } from '@/types';

const geoUrl =
  'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

interface WorldMapProps {
  countries: Country[];
  selectedCountry: Country | null;
  onCountrySelect: (country: Country) => void;
}

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
  'MY': 'MYS',
  'CH': 'CHE',
  'NO': 'NOR',
  'SE': 'SWE',
  'PL': 'POL',
  'UA': 'UKR',
  'BE': 'BEL',
  'PT': 'PRT',
  'PH': 'PHL',
  'PK': 'PAK',
  'BD': 'BGD',
  'IL': 'ISR',
  'NZ': 'NZL',
  'CL': 'CHL',
  'CO': 'COL',
  'PE': 'PER',
  'NG': 'NGA',
  'EG': 'EGY',
  'KE': 'KEN',
  'MA': 'MAR',
  'FI': 'FIN',
  'DK': 'DNK',
  'AT': 'AUT',
  'GR': 'GRC',
  'CZ': 'CZE',
  'RO': 'ROU',
  'KZ': 'KAZ',
  'LK': 'LKA',
  'KH': 'KHM',
  'MN': 'MNG',
  'PA': 'PAN',
  'CR': 'CRI',
  'EC': 'ECU',
  'UY': 'URY',
  'GH': 'GHA',
  'ET': 'ETH',
  'QA': 'QAT',
  'KW': 'KWT',
  'OM': 'OMN',
  'JO': 'JOR'

};

const reverseCountryCodeMap: Record<string, string> =
  Object.fromEntries(
    Object.entries(countryCodeMap).map(([k, v]) => [v, k])
  );

/* ✅ Risk color scale (same like previous logic) */
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

export function WorldMap({
  countries,
  selectedCountry,
  onCountrySelect
}: WorldMapProps) {

  const [tooltip, setTooltip] = useState<{
    content: string;
    x: number;
    y: number;
  } | null>(null);

  const [hoveredGeoId, setHoveredGeoId] =
    useState<string | null>(null);

  const countryMap = useMemo(() => {
    return new Map(countries.map(c => [c.id, c]));
  }, [countries]);

  const getCountryRisk = (
    geoId: string
  ): Country | undefined => {
    const code = reverseCountryCodeMap[geoId];
    return code ? countryMap.get(code) : undefined;
  };

  const isSelected = (geoId: string) => {
    if (!selectedCountry) return false;
    return countryCodeMap[selectedCountry.id] === geoId;
  };

  return (
    <div className="relative w-full h-full bg-[#0b1220] overflow-hidden">

      <ComposableMap
        projection="geoMercator"
        projectionConfig={{
          scale: 140,
          center: [0, 25]
        }}
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

                  stroke={
                    selected
                      ? '#2563eb'
                      : '#1f2a44'
                  }

                  strokeWidth={
                    selected ? 1.8 : 0.6
                  }

                  style={{
                    default: {
                      fill: isHovered
                        ? '#0f1f3d'
                        : '#16233a',

                      outline: 'none',

                      transition:
                        'fill 0.35s cubic-bezier(0.4,0,0.2,1), filter 0.35s ease, stroke 0.35s ease',

                      filter:
                        isHovered
                          ? 'brightness(1.15)'
                          : 'none'
                    },
                    hover: {
                      outline: 'none'
                    },
                    pressed: {
                      outline: 'none'
                    }
                  }}

                  onMouseEnter={(e) => {
                    setHoveredGeoId(geo.id);
                    const country = getCountryRisk(geo.id);
                    if (country) {
                      setTooltip({
                        content: `${country.name} - Risk: ${country.risk_score}`,
                        x: e.clientX + 12,
                        y: e.clientY - 32
                      });
                    }
                  }}

                  onMouseLeave={() => {
                    setHoveredGeoId(null);
                    setTooltip(null);
                  }}

                  onClick={() => {
                    const country = getCountryRisk(geo.id);
                    if (country) {
                      onCountrySelect(country);
                    }
                  }}
                />
              );
            })
          }
        </Geographies>

        {/* ✅ RISK BASED MARKERS */}
        {countries.map((country) => {

          const markerColor =
            riskColorScale(country.risk_score);

          const isActive =
            selectedCountry?.id === country.id;

          return (
            <Marker
              key={country.id}
              coordinates={[
                country.coordinates.lng,
                country.coordinates.lat
              ]}
            >
              <circle
                r={isActive ? 7 : 5}
                fill={markerColor}
                stroke="#0b1220"
                strokeWidth={2}
                style={{
                  transition:
                    'all 0.3s ease',

                  filter: isActive
                    ? `drop-shadow(0 0 14px ${markerColor})`
                    : `drop-shadow(0 0 6px ${markerColor})`
                }}
                className="cursor-pointer"
                onClick={() =>
                  onCountrySelect(country)
                }
                onMouseEnter={(e) => {
                  setTooltip({
                    content: `${country.name} - Risk: ${country.risk_score}`,
                    x: e.clientX + 12,
                    y: e.clientY - 32
                  });
                }}
                onMouseLeave={() =>
                  setTooltip(null)
                }
              />
            </Marker>
          );
        })}

      </ComposableMap>

      {/* TOOLTIP */}
      {tooltip && (
        <div
          className="fixed z-50 px-3 py-2 text-sm bg-[#111827] border border-[#1f2a44] rounded-md shadow-lg pointer-events-none text-slate-300 backdrop-blur-sm"
          style={{
            left: tooltip.x,
            top: tooltip.y
          }}
        >
          {tooltip.content}
        </div>
      )}
    </div>
  );
}