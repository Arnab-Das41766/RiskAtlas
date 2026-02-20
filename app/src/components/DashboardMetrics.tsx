import { useState, useEffect } from 'react';
import { 
  Globe, 
  AlertTriangle, 
  FileText, 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Activity,
  Link2
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { getDashboardMetrics } from '@/services/api';
import type { DashboardMetrics as DashboardMetricsType } from '@/types';

export function DashboardMetrics() {
  const [metrics, setMetrics] = useState<DashboardMetricsType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const loadMetrics = async () => {
    try {
      const data = await getDashboardMetrics();
      setMetrics(data);
    } catch (err) {
      console.error('Failed to load metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="bg-slate-900/50 border-slate-700">
            <CardContent className="p-4">
              <div className="animate-pulse h-16 bg-slate-800 rounded" />
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (!metrics) return null;

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

  const metricCards = [
    {
      icon: Globe,
      label: 'Countries Monitored',
      value: metrics.total_countries_monitored,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/20',
      trend: null
    },
    {
      icon: AlertTriangle,
      label: 'High Risk Countries',
      value: metrics.high_risk_countries,
      color: 'text-red-400',
      bgColor: 'bg-red-500/20',
      trend: null
    },
    {
      icon: FileText,
      label: 'Policy Alerts',
      value: metrics.policy_alerts_this_week,
      color: 'text-orange-400',
      bgColor: 'bg-orange-500/20',
      trend: null
    },
    {
      icon: Activity,
      label: 'Avg Global Risk',
      value: metrics.avg_global_risk,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/20',
      suffix: '/100',
      trend: null
    },
    {
      icon: TrendingUp,
      label: 'Risk Trend',
      value: metrics.top_risk_trend.charAt(0).toUpperCase() + metrics.top_risk_trend.slice(1),
      color: getTrendColor(metrics.top_risk_trend),
      bgColor: metrics.top_risk_trend === 'increasing' ? 'bg-red-500/20' : metrics.top_risk_trend === 'decreasing' ? 'bg-green-500/20' : 'bg-yellow-500/20',
      trend: metrics.top_risk_trend,
      isText: true
    },
    {
      icon: Link2,
      label: 'Supply Chain Alerts',
      value: metrics.supply_chain_alerts,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/20',
      trend: null
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {metricCards.map((card, index) => (
        <Card key={index} className="bg-slate-900/50 border-slate-700 hover:border-slate-600 transition-colors">
          <CardContent className="p-4">
            <div className="flex items-start justify-between">
              <div className={`p-2 rounded-lg ${card.bgColor}`}>
                <card.icon className={`w-4 h-4 ${card.color}`} />
              </div>
              {card.trend && getTrendIcon(card.trend)}
            </div>
            <div className="mt-3">
              <p className="text-2xl font-bold text-white">
                {card.value}{card.suffix || ''}
              </p>
              <p className="text-xs text-slate-400 mt-1">{card.label}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
