import { useState, useEffect } from 'react';
import { 
  Calculator, 
  DollarSign, 
  Percent, 
  ArrowRight, 
  AlertCircle, 
  Brain,
  TrendingUp,
  TrendingDown,
  Factory,
  Shield
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { simulateCost, getIndustries } from '@/services/api';
import type { CostSimulationResponse } from '@/types';

interface CostSimulatorProps {
  selectedCountryId?: string;
  defaultTariff?: number;
}

export function CostSimulator({ selectedCountryId, defaultTariff = 15 }: CostSimulatorProps) {
  const [baseCost, setBaseCost] = useState<string>('');
  const [tariffPercentage, setTariffPercentage] = useState<string>(defaultTariff.toString());
  const [selectedIndustry, setSelectedIndustry] = useState<string>('');
  const [industries, setIndustries] = useState<string[]>([]);
  const [result, setResult] = useState<CostSimulationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadIndustries();
  }, []);

  useEffect(() => {
    if (defaultTariff) {
      setTariffPercentage(defaultTariff.toString());
    }
  }, [defaultTariff]);

  const loadIndustries = async () => {
    try {
      const data = await getIndustries();
      setIndustries(data.industries);
    } catch (err) {
      console.error('Failed to load industries:', err);
    }
  };

  const handleSimulate = async () => {
    const base = parseFloat(baseCost);
    const tariff = parseFloat(tariffPercentage);

    if (isNaN(base) || base <= 0) {
      setError('Please enter a valid base cost');
      return;
    }
    if (isNaN(tariff) || tariff < 0) {
      setError('Please enter a valid tariff percentage');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const response = await simulateCost({
        base_cost: base,
        tariff_percentage: tariff,
        country_id: selectedCountryId,
        industry: selectedIndustry || undefined,
      });
      setResult(response);
    } catch (err) {
      setError('Failed to simulate cost. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getTrendIcon = (trend: string) => {
    if (trend === 'increasing') return <TrendingUp className="w-4 h-4 text-red-500" />;
    if (trend === 'decreasing') return <TrendingDown className="w-4 h-4 text-green-500" />;
    return null;
  };

  return (
    <Card className="bg-slate-900/50 border-slate-700">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <Calculator className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-white">
                Predictive Cost Simulator
              </CardTitle>
              <p className="text-sm text-slate-400">
                AI-powered cost impact analysis
              </p>
            </div>
          </div>
          <Badge variant="outline" className="bg-purple-500/10 text-purple-400 border-purple-500/50">
            <Brain className="w-3 h-3 mr-1" />
            AI Enhanced
          </Badge>
        </div>
      </CardHeader>

      <CardContent>
        <Tabs defaultValue="calculator" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-slate-800">
            <TabsTrigger value="calculator">Calculator</TabsTrigger>
            <TabsTrigger value="ai-prediction" disabled={!result?.ai_prediction}>
              AI Prediction
            </TabsTrigger>
          </TabsList>

          <TabsContent value="calculator" className="mt-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Input Section */}
              <div className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="baseCost" className="text-slate-300 flex items-center gap-2">
                      <DollarSign className="w-4 h-4" />
                      Base Product Cost
                    </Label>
                    <Input
                      id="baseCost"
                      type="number"
                      placeholder="Enter amount"
                      value={baseCost}
                      onChange={(e) => setBaseCost(e.target.value)}
                      className="bg-slate-800 border-slate-600 text-white placeholder:text-slate-500"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="tariff" className="text-slate-300 flex items-center gap-2">
                      <Percent className="w-4 h-4" />
                      Tariff %
                    </Label>
                    <Input
                      id="tariff"
                      type="number"
                      placeholder="Enter %"
                      value={tariffPercentage}
                      onChange={(e) => setTariffPercentage(e.target.value)}
                      className="bg-slate-800 border-slate-600 text-white placeholder:text-slate-500"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="industry" className="text-slate-300 flex items-center gap-2">
                    <Factory className="w-4 h-4" />
                    Industry (Optional)
                  </Label>
                  <Select value={selectedIndustry} onValueChange={setSelectedIndustry}>
                    <SelectTrigger className="bg-slate-800 border-slate-600 text-white">
                      <SelectValue placeholder="Select industry for supply chain analysis" />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-800 border-slate-600">
                      {industries.map((industry) => (
                        <SelectItem key={industry} value={industry} className="text-white">
                          {industry}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {error && (
                  <div className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/50 rounded-lg">
                    <AlertCircle className="w-4 h-4 text-red-500" />
                    <p className="text-sm text-red-400">{error}</p>
                  </div>
                )}

                <Button
                  onClick={handleSimulate}
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Calculating...
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      Calculate Final Cost
                      <ArrowRight className="w-4 h-4" />
                    </span>
                  )}
                </Button>
              </div>

              {/* Results Section */}
              <div className={`p-4 rounded-lg border transition-all duration-300 ${
                result 
                  ? 'bg-slate-800/50 border-slate-600' 
                  : 'bg-slate-800/20 border-slate-700/50'
              }`}>
                {result ? (
                  <div className="space-y-3">
                    <h4 className="text-sm font-semibold text-slate-300 mb-3">
                      Cost Breakdown
                    </h4>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-slate-400">Base Cost</span>
                        <span className="text-sm font-medium text-white">
                          ${result.base_cost.toLocaleString()}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-slate-400">
                          Tariff ({result.tariff_percentage}%)
                        </span>
                        <span className="text-sm font-medium text-orange-400">
                          +${result.tariff_amount.toLocaleString()}
                        </span>
                      </div>
                      
                      {result.risk_adjustment && result.risk_adjustment > 0 && (
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-slate-400 flex items-center gap-2">
                            <Shield className="w-3 h-3" />
                            Risk Premium
                            <Badge variant="outline" className="text-xs bg-red-500/10 text-red-400 border-red-500/50">
                              High Risk
                            </Badge>
                          </span>
                          <span className="text-sm font-medium text-red-400">
                            +${result.risk_adjustment.toLocaleString()}
                          </span>
                        </div>
                      )}
                      
                      {result.supply_chain_premium && result.supply_chain_premium > 0 && (
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-slate-400 flex items-center gap-2">
                            <Factory className="w-3 h-3" />
                            Supply Chain Premium
                          </span>
                          <span className="text-sm font-medium text-purple-400">
                            +${result.supply_chain_premium.toLocaleString()}
                          </span>
                        </div>
                      )}
                      
                      <div className="h-px bg-slate-700 my-2" />
                      
                      <div className="flex justify-between items-center">
                        <span className="text-base font-semibold text-white">Final Cost</span>
                        <span className="text-xl font-bold text-green-400">
                          ${result.final_cost.toLocaleString()}
                        </span>
                      </div>
                    </div>

                    <div className="mt-3 p-2 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                      <p className="text-xs text-blue-300">
                        Total increase: {((result.final_cost / result.base_cost - 1) * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center h-full py-8 text-center">
                    <Calculator className="w-12 h-12 text-slate-600 mb-3" />
                    <p className="text-sm text-slate-500">
                      Enter values and click Calculate
                    </p>
                  </div>
                )}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="ai-prediction" className="mt-4">
            {result?.ai_prediction && (
              <div className="space-y-4">
                <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Brain className="w-4 h-4 text-purple-400" />
                    <span className="text-sm font-medium text-purple-400">
                      AI Cost Prediction (3 Months)
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-400">Predicted Risk Score</span>
                    <div className="flex items-center gap-2">
                      <span className="text-lg font-bold text-white">
                        {result.ai_prediction.predicted_risk_3m}
                      </span>
                      {getTrendIcon(result.ai_prediction.trend)}
                    </div>
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-sm text-slate-400">Confidence</span>
                    <span className="text-sm text-slate-300">
                      {result.ai_prediction.confidence}%
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 bg-slate-800/50 rounded-lg text-center">
                    <p className="text-xs text-slate-500 mb-1">3 Months</p>
                    <p className="text-lg font-bold text-white">
                      ${(result.base_cost * (1 + result.ai_prediction.estimated_future_tariff / 100)).toFixed(0)}
                    </p>
                  </div>
                  <div className="p-3 bg-slate-800/50 rounded-lg text-center">
                    <p className="text-xs text-slate-500 mb-1">6 Months</p>
                    <p className="text-lg font-bold text-slate-300">
                      Risk: {result.ai_prediction.predicted_risk_6m}
                    </p>
                  </div>
                  <div className="p-3 bg-slate-800/50 rounded-lg text-center">
                    <p className="text-xs text-slate-500 mb-1">12 Months</p>
                    <p className="text-lg font-bold text-slate-300">
                      Risk: {result.ai_prediction.predicted_risk_12m}
                    </p>
                  </div>
                </div>

                <div className="p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                  <p className="text-xs text-yellow-300/70">
                    <strong>AI Recommendation:</strong> Based on the predicted trend, 
                    consider {result.ai_prediction.trend === 'increasing' ? 'diversifying suppliers or negotiating long-term contracts' : 'maintaining current supplier relationships'} 
                    to optimize costs.
                  </p>
                </div>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
