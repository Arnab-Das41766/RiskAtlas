import { useState, useEffect } from 'react';
import { Bell, Filter, AlertTriangle, AlertCircle, Info, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { getPolicyAlerts } from '@/services/api';
import type { PolicyAlert } from '@/types';

interface PolicyAlertsFeedProps {
  selectedCountry?: string;
}

export function PolicyAlertsFeed({ selectedCountry }: PolicyAlertsFeedProps) {
  const [alerts, setAlerts] = useState<PolicyAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    loadAlerts();
  }, [selectedCountry]);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const data = await getPolicyAlerts(
        selectedCountry,
        filter === 'all' ? undefined : filter
      );
      setAlerts(data);
    } catch (err) {
      console.error('Failed to load policy alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  const getImpactIcon = (impact: string) => {
    switch (impact) {
      case 'High':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'Medium':
        return <AlertCircle className="w-4 h-4 text-orange-500" />;
      default:
        return <Info className="w-4 h-4 text-blue-500" />;
    }
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'High':
        return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'Medium':
        return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      default:
        return 'bg-blue-500/20 text-blue-400 border-blue-500/50';
    }
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      'Export Control': 'bg-purple-500/20 text-purple-400',
      'Export Restriction': 'bg-red-500/20 text-red-400',
      'Tariff': 'bg-orange-500/20 text-orange-400',
      'Subsidy': 'bg-green-500/20 text-green-400',
      'Incentive': 'bg-emerald-500/20 text-emerald-400',
      'Policy': 'bg-blue-500/20 text-blue-400',
      'Regulation': 'bg-cyan-500/20 text-cyan-400',
    };
    return colors[category] || 'bg-slate-500/20 text-slate-400';
  };

  const categories = ['all', 'Export Control', 'Tariff', 'Subsidy', 'Policy', 'Regulation'];

  return (
    <Card className="bg-slate-900/50 border-slate-700 h-full flex flex-col overflow-hidden">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-red-500/20 rounded-lg">
              <Bell className="w-5 h-5 text-red-400" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-white">
                Policy Alerts
              </CardTitle>
              <p className="text-xs text-slate-400">
                Real-time trade policy updates
              </p>
            </div>
          </div>
          <Badge variant="outline" className="bg-red-500/10 text-red-400 border-red-500/50 animate-pulse">
            LIVE
          </Badge>
        </div>

        {/* Filter Buttons */}
        <div className="flex items-center gap-2 mt-3 overflow-x-auto pb-2">
          <Filter className="w-4 h-4 text-slate-500 flex-shrink-0" />
          {categories.map((cat) => (
            <Button
              key={cat}
              variant={filter === cat ? 'default' : 'outline'}
              size="sm"
              onClick={() => {
                setFilter(cat);
                loadAlerts();
              }}
              className={`text-xs capitalize whitespace-nowrap ${filter === cat
                  ? 'bg-blue-600 hover:bg-blue-700'
                  : 'bg-slate-800 border-slate-600 text-slate-400 hover:text-white'
                }`}
            >
              {cat}
            </Button>
          ))}
        </div>
      </CardHeader>

      <CardContent className="p-0">
        <ScrollArea className="h-[400px] px-4">
          {loading ? (
            <div className="space-y-3 p-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="animate-pulse h-24 bg-slate-800 rounded-lg" />
              ))}
            </div>
          ) : alerts.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-center p-4">
              <Bell className="w-12 h-12 text-slate-600 mb-3" />
              <p className="text-sm text-slate-400">No policy alerts found</p>
            </div>
          ) : (
            <div className="space-y-3 pb-4">
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className="p-4 bg-slate-800/50 rounded-lg border border-slate-700 hover:border-slate-600 transition-all cursor-pointer group"
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5">
                      {getImpactIcon(alert.impact)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <h4 className="text-sm font-medium text-white group-hover:text-blue-400 transition-colors line-clamp-2">
                          {alert.title}
                        </h4>
                        <ExternalLink className="w-4 h-4 text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
                      </div>

                      <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                        {alert.description}
                      </p>

                      <div className="flex items-center gap-2 mt-3 flex-wrap">
                        <Badge
                          variant="outline"
                          className={`text-xs ${getImpactColor(alert.impact)}`}
                        >
                          {alert.impact} Impact
                        </Badge>
                        <Badge
                          variant="outline"
                          className={`text-xs ${getCategoryColor(alert.category)}`}
                        >
                          {alert.category}
                        </Badge>
                        <span className="text-xs text-slate-500">
                          {alert.date}
                        </span>
                      </div>

                      {alert.affected_industries.length > 0 && (
                        <div className="flex items-center gap-1 mt-2 flex-wrap">
                          <span className="text-xs text-slate-500">Affects:</span>
                          {alert.affected_industries.slice(0, 3).map((industry, idx) => (
                            <span key={idx} className="text-xs text-slate-400">
                              {industry}{idx < Math.min(alert.affected_industries.length, 3) - 1 ? ', ' : ''}
                            </span>
                          ))}
                          {alert.affected_industries.length > 3 && (
                            <span className="text-xs text-slate-500">
                              +{alert.affected_industries.length - 3} more
                            </span>
                          )}
                        </div>
                      )}
                    </div>
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
