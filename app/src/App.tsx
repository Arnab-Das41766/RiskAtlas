import { useState, useEffect } from 'react';
import {
  Globe,
  Shield,
  Activity,
  Zap,
  Menu,
  X
} from 'lucide-react';
import { WorldMap } from '@/components/WorldMap';
import { CountryInfoPanel } from '@/components/CountryInfoPanel';
import { CostSimulator } from '@/components/CostSimulator';
import { DashboardMetrics } from '@/components/DashboardMetrics';
import { PolicyAlertsFeed } from '@/components/PolicyAlertsFeed';
import { AIForecasting } from '@/components/AIForecasting';
import { SupplyChainVulnerability } from '@/components/SupplyChainVulnerability';
import { AlternativeSuppliers } from '@/components/AlternativeSuppliers';
import { getCountries, getCountry } from '@/services/api';
import type { Country, CountryDetail } from '@/types';
import './App.css';

function App() {
  const [countries, setCountries] = useState<Country[]>([]);
  const [selectedCountry, setSelectedCountry] = useState<Country | null>(null);
  const [countryDetail, setCountryDetail] = useState<CountryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    loadCountries();
  }, []);

  const loadCountries = async () => {
    try {
      setLoading(true);
      const data = await getCountries();
      setCountries(data);
      setError(null);
    } catch (err) {
      setError('Failed to load countries. Please ensure the backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleCountrySelect = async (country: Country) => {
    setSelectedCountry(country);
    setDetailLoading(true);
    try {
      const detail = await getCountry(country.id);
      setCountryDetail(detail);
    } catch (err) {
      console.error('Failed to load country details:', err);
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 grid-bg">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">RiskAtlas</h1>
                <p className="text-xs text-slate-400">Trade Risk Intelligence Platform</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/30 rounded-full">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-xs text-green-400">Live Monitoring</span>
              </div>

              <div className="hidden sm:flex items-center gap-2 text-sm text-slate-400">
                <Activity className="w-4 h-4 text-blue-400" />
                <span>{countries.length} Countries</span>
              </div>

              <button
                className="lg:hidden p-2 text-slate-400 hover:text-white"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-[1920px] mx-auto p-4 sm:p-6 lg:p-8">
        {error ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg mb-4">
              <Activity className="w-8 h-8 text-red-500" />
            </div>
            <h2 className="text-lg font-semibold text-white mb-2">Connection Error</h2>
            <p className="text-sm text-slate-400 max-w-md mb-4">{error}</p>
            <button
              onClick={loadCountries}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              Retry Connection
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Dashboard Metrics */}
            <DashboardMetrics />

            {/* Main Grid */}
            <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
              {/* Left Column - Map & Cost Simulator */}
              <div className="xl:col-span-7 space-y-6">
                {/* World Map */}
                <div className="bg-slate-900/50 border border-slate-700 rounded-xl overflow-hidden" style={{ height: '550px' }}>
                  <div className="p-4 border-b border-slate-800 flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                      <Globe className="w-5 h-5 text-blue-400" />
                      Global Risk Intelligence Map
                    </h2>
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                      <Zap className="w-4 h-4 text-yellow-400" />
                      <span className="hidden sm:inline">Real-time Data</span>
                    </div>
                  </div>
                  <div className="h-[calc(100%-65px)]">
                    {loading ? (
                      <div className="flex items-center justify-center h-full">
                        <div className="flex flex-col items-center gap-4">
                          <div className="w-12 h-12 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin" />
                          <p className="text-sm text-slate-400">Loading intelligence data...</p>
                        </div>
                      </div>
                    ) : (
                      <WorldMap
                        countries={countries}
                        selectedCountry={selectedCountry}
                        onCountrySelect={handleCountrySelect}
                      />
                    )}
                  </div>
                </div>

                {/* Cost Simulator */}
                <CostSimulator
                  selectedCountryId={selectedCountry?.id}
                  defaultTariff={selectedCountry?.tariff_percentage}
                />
              </div>

              {/* Right Column - Info Panels */}
              <div className="xl:col-span-5 space-y-6">
                {/* Country Info Panel */}
                <div className="h-[500px] overflow-hidden">
                  <CountryInfoPanel
                    country={countryDetail}
                    loading={detailLoading}
                  />
                </div>

                {/* AI Forecasting */}
                <div className="h-[380px] overflow-hidden">
                  <AIForecasting country={countryDetail} />
                </div>
              </div>
            </div>

            {/* Bottom Row - Additional Intelligence */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Policy Alerts */}
              <div className="h-[450px] overflow-hidden">
                <PolicyAlertsFeed selectedCountry={selectedCountry?.id} />
              </div>

              {/* Supply Chain Vulnerability */}
              <div className="h-[450px] overflow-hidden">
                <SupplyChainVulnerability />
              </div>

              {/* Alternative Suppliers */}
              <div className="h-[450px] overflow-hidden">
                <AlternativeSuppliers selectedCountry={selectedCountry} />
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/50 mt-8">
        <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-blue-500" />
              <p className="text-sm text-slate-500">
                RiskAtlas - Trade Risk Intelligence Platform
              </p>
            </div>
            <div className="flex items-center gap-6 text-sm text-slate-500">
              <span>Last updated: {new Date().toLocaleString()}</span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-green-500 rounded-full" />
                System Operational
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
