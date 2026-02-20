import type {
  Country,
  CountryDetail,
  CostSimulationRequest,
  CostSimulationResponse,
  PolicyAlert,
  SupplyChainInfo,
  AlternativeSupplier,
  DashboardMetrics,
  Industry
} from '@/types';

const API_BASE_URL = 'http://localhost:8000';

// Dashboard
export async function getDashboardMetrics(): Promise<DashboardMetrics> {
  const response = await fetch(`${API_BASE_URL}/dashboard-metrics`);
  if (!response.ok) {
    throw new Error('Failed to fetch dashboard metrics');
  }
  return response.json();
}

// Countries
export async function getCountries(industry?: string, riskLevel?: string): Promise<Country[]> {
  let url = `${API_BASE_URL}/countries`;
  const params = new URLSearchParams();
  if (industry) params.append('industry', industry);
  if (riskLevel) params.append('risk_level', riskLevel);
  if (params.toString()) url += `?${params.toString()}`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch countries');
  }
  return response.json();
}

export async function getCountry(id: string): Promise<CountryDetail> {
  const response = await fetch(`${API_BASE_URL}/country/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch country details');
  }
  return response.json();
}

// Policy Alerts
export async function getPolicyAlerts(
  country?: string,
  category?: string,
  impact?: string
): Promise<PolicyAlert[]> {
  let url = `${API_BASE_URL}/policy-alerts`;
  const params = new URLSearchParams();
  if (country) params.append('country', country);
  if (category) params.append('category', category);
  if (impact) params.append('impact', impact);
  if (params.toString()) url += `?${params.toString()}`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch policy alerts');
  }
  return response.json();
}

// Supply Chain
export async function getSupplyChainInfo(industry: string): Promise<SupplyChainInfo> {
  const response = await fetch(`${API_BASE_URL}/supply-chain/${industry}`);
  if (!response.ok) {
    throw new Error('Failed to fetch supply chain info');
  }
  return response.json();
}

// Industries
export async function getIndustries(): Promise<Industry> {
  const response = await fetch(`${API_BASE_URL}/industries`);
  if (!response.ok) {
    throw new Error('Failed to fetch industries');
  }
  return response.json();
}

// Alternative Suppliers
export async function getAlternativeSuppliers(
  countryId: string,
  industry?: string
): Promise<AlternativeSupplier[]> {
  let url = `${API_BASE_URL}/alternative-suppliers/${countryId}`;
  if (industry) url += `?industry=${industry}`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch alternative suppliers');
  }
  return response.json();
}

// Cost Simulation
export async function simulateCost(data: CostSimulationRequest): Promise<CostSimulationResponse> {
  const response = await fetch(`${API_BASE_URL}/simulate-cost`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('Failed to simulate cost');
  }
  return response.json();
}
