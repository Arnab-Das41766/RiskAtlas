import { Brain, TrendingUp, TrendingDown, Minus, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import type { CountryDetail } from '@/types';

interface AIForecastingProps {
  country: CountryDetail | null;
}

export function AIForecasting({ country }: AIForecastingProps) {
  if (!country || !country.ai_forecast) {
    return (
      <Card className="bg-slate-900/50 border-slate-700 h-full">
        <CardContent className="flex flex-col items-center justify-center h-full p-6 text-center">
          <Brain className="w-12 h-12 text-slate-600 mb-3" />
          <h3 className="text-sm font-medium text-slate-400">
            Select a country to view AI predictions
          </h3>
        </CardContent>
      </Card>
    );
  }

  const forecast = country.ai_forecast;
  const currentScore = country.risk_score;

  const getTrendIcon = (trend: string) => {
    if (trend === 'increasing') return <TrendingUp className="w-4 h-4 text-red-500" />;
    if (trend === 'decreasing') return <TrendingDown className="w-4 h-4 text-green-500" />;
    return <Minus className="w-4 h-4 text-yellow-500" />;
  };

  const getTrendColor = (trend: string) => {
    if (trend === 'increasing') return 'text-red-400';
    if (trend === 'decreasing') return 'text-green-400';
    return 'text-yellow-400';
  };

  const getRiskLevelColor = (score: number) => {
    if (score <= 40) return 'text-green-400';
    if (score <= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const periods = [
    { key: '3_month', label: '3 Months', timeframe: 'Short-term' },
    { key: '6_month', label: '6 Months', timeframe: 'Medium-term' },
    { key: '12_month', label: '12 Months', timeframe: 'Long-term' }
  ];

  return (
    <Card className="bg-slate-900/50 border-slate-700 h-full flex flex-col overflow-hidden">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-500/20 rounded-lg">
              <Brain className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-white">
                AI Risk Forecast
              </CardTitle>
              <p className="text-xs text-slate-400">
                ML-powered geopolitical predictions
              </p>
            </div>
          </div>
          <Badge variant="outline" className="bg-purple-500/10 text-purple-400 border-purple-500/50">
            <CheckCircle2 className="w-3 h-3 mr-1" />
            AI Powered
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-auto">
        <div className="space-y-4">
          {/* Current Status */}
          <div className="p-3 bg-slate-800/50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-slate-400">Current Risk Score</span>
              <span className={`text-lg font-bold ${getRiskLevelColor(currentScore)}`}>
                {currentScore}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500">Trend:</span>
              {getTrendIcon(country.risk_trend || 'stable')}
              <span className={`text-xs ${getTrendColor(country.risk_trend || 'stable')}`}>
                {country.risk_trend?.charAt(0).toUpperCase()}{country.risk_trend?.slice(1) || 'Stable'}
              </span>
            </div>
          </div>

          {/* Forecast Periods */}
          <div className="space-y-3">
            {periods.map((period) => {
              const data = forecast[period.key as keyof typeof forecast];
              if (!data) return null;

              const scoreChange = data.score - currentScore;

              return (
                <div key={period.key} className="p-3 bg-slate-800/30 rounded-lg border border-slate-700/50">
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <span className="text-sm font-medium text-white">{period.label}</span>
                      <span className="text-xs text-slate-500 ml-2">({period.timeframe})</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`text-lg font-bold ${getRiskLevelColor(data.score)}`}>
                        {data.score}
                      </span>
                      {scoreChange !== 0 && (
                        <span className={`text-xs ${scoreChange > 0 ? 'text-red-400' : 'text-green-400'}`}>
                          {scoreChange > 0 ? '+' : ''}{scoreChange}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {getTrendIcon(data.trend)}
                      <span className={`text-xs ${getTrendColor(data.trend)}`}>
                        {data.trend.charAt(0).toUpperCase()}{data.trend.slice(1)}
                      </span>
                    </div>
                  </div>

                  {/* Confidence Bar */}
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500">Confidence:</span>
                    <div className="flex-1">
                      <Progress
                        value={data.confidence}
                        className="h-1.5 bg-slate-700"
                      />
                    </div>
                    <span className="text-xs text-slate-400">{data.confidence}%</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* AI Disclaimer */}
          <div className="flex items-start gap-2 p-2 bg-purple-500/10 border border-purple-500/20 rounded-lg">
            <AlertCircle className="w-4 h-4 text-purple-400 mt-0.5 flex-shrink-0" />
            <p className="text-xs text-purple-300/70">
              Predictions are based on historical data, current geopolitical trends,
              and machine learning models. Confidence decreases for longer timeframes.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
