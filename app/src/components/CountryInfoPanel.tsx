import { AlertTriangle, TrendingUp, FileText, Globe, Newspaper, Factory, Shield, MapPin } from 'lucide-react';
import type { CountryDetail } from '@/types';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';

interface CountryInfoPanelProps {
  country: CountryDetail | null;
  loading?: boolean;
}

export function CountryInfoPanel({ country, loading }: CountryInfoPanelProps) {
  if (loading) {
    return (
      <Card className="h-full bg-slate-900/50 border-slate-700">
        <CardContent className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-slate-800 rounded w-2/3" />
            <div className="h-4 bg-slate-800 rounded w-full" />
            <div className="h-4 bg-slate-800 rounded w-3/4" />
            <div className="h-32 bg-slate-800 rounded" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!country) {
    return (
      <Card className="h-full bg-slate-900/50 border-slate-700">
        <CardContent className="flex flex-col items-center justify-center h-full p-6 text-center">
          <Globe className="w-16 h-16 text-slate-600 mb-4" />
          <h3 className="text-lg font-semibold text-slate-400 mb-2">
            Select a Country
          </h3>
          <p className="text-sm text-slate-500">
            Click on a country on the map to view detailed trade risk intelligence
          </p>
        </CardContent>
      </Card>
    );
  }

  const getRiskColor = (score: number) => {
    if (score <= 40) return 'text-green-400';
    if (score <= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRiskBgColor = (score: number) => {
    if (score <= 40) return 'bg-green-500/20 border-green-500/50';
    if (score <= 70) return 'bg-yellow-500/20 border-yellow-500/50';
    return 'bg-red-500/20 border-red-500/50';
  };

  const getTrendIcon = (trend?: string) => {
    if (trend === 'increasing') return <TrendingUp className="w-4 h-4 text-red-400" />;
    if (trend === 'decreasing') return <TrendingUp className="w-4 h-4 text-green-400 rotate-180" />;
    return null;
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      'Policy': 'bg-blue-500/20 text-blue-400 border-blue-500/50',
      'Tariff': 'bg-orange-500/20 text-orange-400 border-orange-500/50',
      'Geopolitics': 'bg-red-500/20 text-red-400 border-red-500/50',
      'Regulation': 'bg-purple-500/20 text-purple-400 border-purple-500/50',
      'Sanctions': 'bg-red-600/20 text-red-500 border-red-600/50',
      'Currency': 'bg-green-500/20 text-green-400 border-green-500/50',
      'Diplomacy': 'bg-cyan-500/20 text-cyan-400 border-cyan-500/50',
      'Industry': 'bg-pink-500/20 text-pink-400 border-pink-500/50',
      'Investment': 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50',
      'Trade Bloc': 'bg-indigo-500/20 text-indigo-400 border-indigo-500/50',
      'Agreement': 'bg-teal-500/20 text-teal-400 border-teal-500/50',
      'Energy': 'bg-amber-500/20 text-amber-400 border-amber-500/50',
      'Trade Flow': 'bg-lime-500/20 text-lime-400 border-lime-500/50',
    };
    return colors[category] || 'bg-slate-500/20 text-slate-400 border-slate-500/50';
  };

  return (
    <Card className="h-full bg-slate-900/50 border-slate-700 overflow-hidden flex flex-col">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <CardTitle className="text-xl font-bold text-white">
                {country.name}
              </CardTitle>
              {getTrendIcon(country.risk_trend)}
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <Badge variant="outline" className="text-xs bg-slate-700/50 text-slate-300">
                <MapPin className="w-3 h-3 mr-1" />
                {country.id}
              </Badge>
              {country.supply_chain_risk && (
                <Badge
                  variant="outline"
                  className={`text-xs ${country.supply_chain_risk === 'High' || country.supply_chain_risk === 'Critical'
                      ? 'bg-red-500/10 text-red-400 border-red-500/50'
                      : 'bg-green-500/10 text-green-400 border-green-500/50'
                    }`}
                >
                  Supply Chain: {country.supply_chain_risk}
                </Badge>
              )}
            </div>
          </div>
          <div className={`px-4 py-2 rounded-lg border-2 ${getRiskBgColor(country.risk_score)}`}>
            <span className="text-xs text-slate-400 block text-center">Risk Score</span>
            <span className={`text-2xl font-bold ${getRiskColor(country.risk_score)}`}>
              {country.risk_score}
            </span>
          </div>
        </div>

        {/* High Risk Alert */}
        {country.risk_score > 70 && (
          <div className="mt-4 flex items-center gap-3 p-3 bg-red-500/10 border border-red-500/50 rounded-lg pulse-risk">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <div>
              <p className="text-sm font-semibold text-red-400">High Risk Warning</p>
              <p className="text-xs text-red-300/70">
                Consider alternative suppliers or friend-shoring options
              </p>
            </div>
          </div>
        )}
      </CardHeader>

      <ScrollArea className="flex-1 px-6 pb-6">
        <div className="space-y-5">
          {/* Key Industries */}
          {country.key_industries && country.key_industries.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Factory className="w-4 h-4 text-slate-400" />
                <h4 className="text-sm font-semibold text-slate-300">Key Industries</h4>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {country.key_industries.map((industry, idx) => (
                  <Badge
                    key={idx}
                    variant="outline"
                    className="text-xs bg-slate-700/50 text-slate-300 border-slate-600"
                  >
                    {industry}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Friend Shore Score */}
          {country.friend_shore_score !== undefined && (
            <div className="p-3 bg-slate-800/50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Shield className="w-4 h-4 text-blue-400" />
                  <span className="text-sm text-slate-300">Friend-Shore Score</span>
                </div>
                <span className={`text-sm font-bold ${country.friend_shore_score >= 80 ? 'text-green-400' :
                    country.friend_shore_score >= 60 ? 'text-yellow-400' : 'text-orange-400'
                  }`}>
                  {country.friend_shore_score}/100
                </span>
              </div>
              <Progress
                value={country.friend_shore_score}
                className="h-2 bg-slate-700"
              />
              <p className="text-xs text-slate-500 mt-1">
                {country.friend_shore_score >= 80
                  ? 'Excellent partner for friend-shoring'
                  : country.friend_shore_score >= 60
                    ? 'Good partner with some considerations'
                    : 'Evaluate carefully for strategic partnerships'}
              </p>
            </div>
          )}

          {/* Tariff Info */}
          <div className="flex items-center gap-4 p-3 bg-slate-800/50 rounded-lg">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <TrendingUp className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-slate-400">Current Tariff Rate</p>
              <p className="text-xl font-bold text-white">{country.tariff_percentage}%</p>
            </div>
          </div>

          <Separator className="bg-slate-700" />

          {/* Trade Policy Summary */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <FileText className="w-4 h-4 text-slate-400" />
              <h4 className="text-sm font-semibold text-slate-300">Trade Policy Summary</h4>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              {country.trade_policy_summary}
            </p>
          </div>

          <Separator className="bg-slate-700" />

          {/* Latest Headlines */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Newspaper className="w-4 h-4 text-slate-400" />
              <h4 className="text-sm font-semibold text-slate-300">Latest Headlines</h4>
            </div>
            <div className="space-y-3">
              {country.headlines.map((headline, index) => (
                <div
                  key={index}
                  className="p-3 bg-slate-800/50 rounded-lg hover:bg-slate-800 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <Badge
                      variant="outline"
                      className={`text-xs ${getCategoryColor(headline.category)}`}
                    >
                      {headline.category}
                    </Badge>
                    <span className="text-xs text-slate-500">{headline.date}</span>
                  </div>
                  <p className="text-sm text-slate-300 font-medium mb-1">
                    {headline.title}
                  </p>
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-slate-500">
                      Source: {headline.source}
                    </p>
                    {headline.impact && (
                      <Badge
                        variant="outline"
                        className={`text-xs ${headline.impact === 'high'
                            ? 'bg-red-500/10 text-red-400 border-red-500/50'
                            : headline.impact === 'medium'
                              ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/50'
                              : 'bg-blue-500/10 text-blue-400 border-blue-500/50'
                          }`}
                      >
                        {headline.impact} impact
                      </Badge>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </ScrollArea>
    </Card>
  );
}
