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
import { CountrySearch } from '@/components/CountrySearch';
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

      {/* 🔥 PREMIUM SEAMLESS NAVBAR */}
      <header className="sticky top-0 z-50 bg-slate-950">
        <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">

            {/* Left Section */}
            <div className="flex items-center gap-4">

              <div className="relative">
                <Shield className="w-7 h-7 text-blue-500" />
                <span className="absolute inset-0 bg-blue-500/20 blur-xl rounded-full"></span>
              </div>

              <div className="flex flex-col leading-tight">
                <h1 className="text-2xl font-semibold tracking-wide text-white">
                  <span className="bg-gradient-to-r from-blue-400 via-blue-500 to-indigo-500 bg-clip-text text-transparent">
                    RISK-ATLAS
                  </span>
                </h1>
                <p className="text-[11px] tracking-widest uppercase text-slate-500">
                  Trade Risk Intelligence Platform
                </p>
              </div>
            </div>

            {/* Right Section */}
            <div className="flex items-center gap-6">

              <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/60 hover:bg-slate-900 transition-colors">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-xs text-green-400">Live Monitoring</span>
              </div>

              <div className="hidden sm:flex items-center gap-2 text-sm text-slate-400">
                <Activity className="w-4 h-4 text-blue-400" />
                <span>{countries.length} Countries</span>
              </div>

              <button
                className="lg:hidden p-2 text-slate-400 hover:text-white transition-colors"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                {sidebarOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
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
            <DashboardMetrics />

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
              <div className="xl:col-span-7 space-y-6">

                <div className="bg-slate-900/50 border border-slate-700 rounded-xl overflow-hidden" style={{ height: '550px' }}>
                  <div className="p-4 border-b border-slate-800 flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                      <Globe className="w-5 h-5 text-blue-400" />
                      Global Risk Intelligence Map
                    </h2>
                    <div className="flex items-center gap-4">
                      <CountrySearch
                        countries={countries}
                        onSelect={handleCountrySelect}
                        selectedCountryId={selectedCountry?.id}
                      />
                      <div className="hidden sm:flex items-center gap-2 text-sm text-slate-400">
                        <Zap className="w-4 h-4 text-yellow-400" />
                        <span>Real-time Data</span>
                      </div>
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

                <CostSimulator
                  selectedCountryId={selectedCountry?.id}
                  defaultTariff={selectedCountry?.tariff_percentage}
                />
              </div>

              <div className="xl:col-span-5 space-y-6">
                <div className="h-[500px] overflow-hidden">
                  <CountryInfoPanel
                    country={countryDetail}
                    loading={detailLoading}
                  />
                </div>

                <div className="h-[380px] overflow-hidden">
                  <AIForecasting country={countryDetail} />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="h-[450px] overflow-hidden">
                <PolicyAlertsFeed selectedCountry={selectedCountry?.id} />
              </div>

              <div className="h-[450px] overflow-hidden">
                <SupplyChainVulnerability />
              </div>

              <div className="h-[450px] overflow-hidden">
                <AlternativeSuppliers selectedCountry={selectedCountry} />
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-slate-800 bg-slate-950/80 backdrop-blur-md mt-12">
  <div className="max-w-[1920px] mx-auto px-6 lg:px-12 py-10">

    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">

      {/* LEFT - BRAND */}
      <div className="flex flex-col gap-2">
        <h2 className="text-xl font-semibold tracking-wide">
          <span className="bg-gradient-to-r from-blue-400 via-blue-500 to-indigo-500 bg-clip-text text-transparent">
            RISK-ATLAS
          </span>
        </h2>
        <p className="text-[11px] tracking-widest uppercase text-slate-500">
          Trade Risk Intelligence Platform
        </p>
        <p className="text-xs text-slate-600 mt-2">
          © {new Date().getFullYear()} RISK-ATLAS. All rights reserved.
        </p>
      </div>

      {/* CENTER - STATUS */}
      <div className="flex flex-col items-start md:items-center gap-3 text-sm text-slate-400">
        <span>
          Last updated: {new Date().toLocaleString()}
        </span>

        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-green-400 font-medium">
            System Operational
          </span>
        </div>
      </div>

      {/* RIGHT - LINKS */}
      <div className="flex flex-col items-start md:items-end gap-3">

        <a
          href="https://github.com/Arnab-Das41766/RiskAtlas"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors duration-300"
        >
          {/* GitHub SVG */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            className="w-5 h-5"
          >
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.26.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.332-1.756-1.332-1.756-1.089-.744.083-.729.083-.729 1.205.085 1.838 1.238 1.838 1.238 1.07 1.835 2.807 1.305 3.492.998.108-.775.418-1.305.762-1.605-2.665-.303-5.467-1.335-5.467-5.932 0-1.31.468-2.38 1.235-3.22-.135-.303-.54-1.52.105-3.165 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.645.24 2.862.12 3.165.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.922.435.375.81 1.096.81 2.21 0 1.596-.015 2.885-.015 3.28 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z" />
          </svg>
          <span>View on GitHub</span>
        </a>

        <span className="text-xs text-slate-600">
          Developed by CODE_PAGLU with ❤️
        </span>

      </div>

    </div>

  </div>
</footer>
    </div>
  );
}

export default App;