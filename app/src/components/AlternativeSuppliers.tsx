import { useState, useEffect } from 'react';
import { ArrowRightLeft, TrendingDown, Shield, MapPin, Star } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { getAlternativeSuppliers } from '@/services/api';
import type { AlternativeSupplier, Country } from '@/types';

interface AlternativeSuppliersProps {
  selectedCountry: Country | null;
}

export function AlternativeSuppliers({ selectedCountry }: AlternativeSuppliersProps) {
  const [alternatives, setAlternatives] = useState<AlternativeSupplier[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedCountry) {
      loadAlternatives();
    } else {
      setAlternatives([]);
    }
  }, [selectedCountry]);

  const loadAlternatives = async () => {
    if (!selectedCountry) return;
    try {
      setLoading(true);
      const data = await getAlternativeSuppliers(selectedCountry.id);
      setAlternatives(data);
    } catch (err) {
      console.error('Failed to load alternative suppliers:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSuitabilityColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-orange-400';
  };

  const getSuitabilityBg = (score: number) => {
    if (score >= 80) return 'bg-green-500/20 border-green-500/50';
    if (score >= 60) return 'bg-yellow-500/20 border-yellow-500/50';
    return 'bg-orange-500/20 border-orange-500/50';
  };

  const getRiskColor = (score: number) => {
    if (score <= 40) return 'text-green-400';
    if (score <= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <Card className="bg-slate-900/50 border-slate-700 h-full flex flex-col overflow-hidden">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-emerald-500/20 rounded-lg">
              <ArrowRightLeft className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-white">
                Alternative Suppliers
              </CardTitle>
              <p className="text-xs text-slate-400">
                Friend-shoring recommendations
              </p>
            </div>
          </div>
        </div>

        {selectedCountry && (
          <div className="mt-3 p-2 bg-slate-800/50 rounded-lg">
            <p className="text-xs text-slate-400">
              Alternatives for: <span className="text-white font-medium">{selectedCountry.name}</span>
            </p>
          </div>
        )}
      </CardHeader>

      <CardContent className="p-0">
        <ScrollArea className="h-[350px] px-4">
          {!selectedCountry ? (
            <div className="flex flex-col items-center justify-center h-64 text-center">
              <MapPin className="w-12 h-12 text-slate-600 mb-3" />
              <p className="text-sm text-slate-400">
                Select a high-risk country to see alternative suppliers
              </p>
            </div>
          ) : loading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="animate-pulse h-32 bg-slate-800 rounded-lg" />
              ))}
            </div>
          ) : alternatives.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-center">
              <Shield className="w-12 h-12 text-green-500 mb-3" />
              <p className="text-sm text-slate-400">
                No alternative suppliers needed
              </p>
              <p className="text-xs text-slate-500 mt-1">
                This country has acceptable risk levels
              </p>
            </div>
          ) : (
            <div className="space-y-3 pb-4">
              {alternatives.map((alt, index) => (
                <div
                  key={alt.country_id}
                  className="p-4 bg-slate-800/50 rounded-lg border border-slate-700 hover:border-slate-600 transition-all"
                >
                  {/* Header */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-lg font-bold text-white">
                        {alt.country_name}
                      </span>
                      {index === 0 && (
                        <Badge className="bg-yellow-500/20 text-yellow-400 border-yellow-500/50">
                          <Star className="w-3 h-3 mr-1" />
                          Top Pick
                        </Badge>
                      )}
                    </div>
                    <div className={`px-3 py-1 rounded-lg border ${getSuitabilityBg(alt.suitability_score)}`}>
                      <span className={`text-sm font-bold ${getSuitabilityColor(alt.suitability_score)}`}>
                        {alt.suitability_score}%
                      </span>
                    </div>
                  </div>

                  {/* Metrics */}
                  <div className="grid grid-cols-3 gap-2 mb-3">
                    <div className="p-2 bg-slate-700/50 rounded">
                      <p className="text-xs text-slate-500">Risk</p>
                      <p className={`text-sm font-bold ${getRiskColor(alt.risk_score)}`}>
                        {alt.risk_score}
                      </p>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <p className="text-xs text-slate-500">Friend Score</p>
                      <p className="text-sm font-bold text-blue-400">
                        {alt.friend_shore_score}
                      </p>
                    </div>
                    <div className="p-2 bg-slate-700/50 rounded">
                      <p className="text-xs text-slate-500">Tariff</p>
                      <p className="text-sm font-bold text-orange-400">
                        {alt.tariff_percentage}%
                      </p>
                    </div>
                  </div>

                  {/* Industries */}
                  <div className="flex flex-wrap gap-1 mb-3">
                    {alt.key_industries.slice(0, 3).map((industry, idx) => (
                      <Badge
                        key={idx}
                        variant="outline"
                        className="text-xs bg-slate-700/50 text-slate-300 border-slate-600"
                      >
                        {industry}
                      </Badge>
                    ))}
                  </div>

                  {/* Reason */}
                  <div className="flex items-start gap-2 p-2 bg-emerald-500/10 rounded-lg">
                    <TrendingDown className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                    <p className="text-xs text-emerald-300/70">{alt.reason}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
