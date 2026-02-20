export interface Headline {
  title: string;
  source: string;
  date: string;
  category: string;
  impact?: string;
}

export interface AIForecast {
  score: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  confidence: number;
}

export interface Country {
  id: string;
  name: string;
  risk_score: number;
  risk_level: 'Low' | 'Medium' | 'High' | 'Critical';
  risk_trend?: 'increasing' | 'decreasing' | 'stable';
  tariff_percentage: number;
  coordinates: {
    lat: number;
    lng: number;
  };
  key_industries?: string[];
  supply_chain_risk?: string;
  friend_shore_score?: number;
}

export interface CountryDetail extends Country {
  trade_policy_summary: string;
  headlines: Headline[];
  ai_forecast?: {
    '3_month'?: AIForecast;
    '6_month'?: AIForecast;
    '12_month'?: AIForecast;
  };
  alternative_to?: string[];
  alternatives?: string[];
}

export interface PolicyAlert {
  id: number;
  title: string;
  country: string;
  category: string;
  impact: 'High' | 'Medium' | 'Low';
  date: string;
  description: string;
  affected_industries: string[];
}

export interface SupplyChainInfo {
  industry: string;
  risk_level: string;
  concentration_risk: string;
  top_suppliers: string[];
  vulnerabilities: string[];
  alternatives_available: boolean;
}

export interface AlternativeSupplier {
  country_id: string;
  country_name: string;
  risk_score: number;
  friend_shore_score: number;
  tariff_percentage: number;
  key_industries: string[];
  suitability_score: number;
  reason: string;
}

export interface CostSimulationRequest {
  base_cost: number;
  tariff_percentage: number;
  country_id?: string;
  industry?: string;
}

export interface AIPrediction {
  predicted_risk_3m: number;
  predicted_risk_6m: number;
  predicted_risk_12m: number;
  confidence: number;
  trend: string;
  estimated_future_tariff: number;
}

export interface CostSimulationResponse {
  base_cost: number;
  tariff_percentage: number;
  tariff_amount: number;
  final_cost: number;
  risk_adjustment?: number;
  supply_chain_premium?: number;
  ai_prediction?: AIPrediction;
}

export interface DashboardMetrics {
  total_countries_monitored: number;
  high_risk_countries: number;
  policy_alerts_this_week: number;
  avg_global_risk: number;
  top_risk_trend: string;
  supply_chain_alerts: number;
}

export interface Industry {
  industries: string[];
  supply_chain_data: string[];
}
