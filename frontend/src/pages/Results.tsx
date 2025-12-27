import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { HiringImpact } from '../api/client';

export default function Results() {
  const navigate = useNavigate();
  const [impact, setImpact] = useState<HiringImpact | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const storedImpact = localStorage.getItem('hiringImpact');
    if (storedImpact) {
      try {
        setImpact(JSON.parse(storedImpact));
      } catch (err) {
        setError('Failed to load results. Please start over.');
      }
    } else {
      setError('No results found. Please start over.');
    }
  }, []);

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'Safe':
        return 'bg-safe text-white';
      case 'Risky':
        return 'bg-risky text-white';
      case 'Dangerous':
        return 'bg-dangerous text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const getRiskEmoji = (riskLevel: string) => {
    switch (riskLevel) {
      case 'Safe':
        return '🟢';
      case 'Risky':
        return '🟡';
      case 'Dangerous':
        return '🔴';
      default:
        return '⚪';
    }
  };

  const getRiskMessage = (riskLevel: string, runwayMonths: number) => {
    switch (riskLevel) {
      case 'Safe':
        return `You have ${runwayMonths.toFixed(1)} months of runway remaining. This is a safe hiring decision.`;
      case 'Risky':
        return `You'll have ${runwayMonths.toFixed(1)} months of runway remaining. Consider your fundraising timeline carefully.`;
      case 'Dangerous':
        return `You'll only have ${runwayMonths.toFixed(1)} months of runway remaining. This is risky - consider delaying the hire or securing funding first.`;
      default:
        return '';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatMonths = (months: number) => {
    if (months >= 999) {
      return '∞ (Profitable)';
    }
    return `${months.toFixed(1)} months`;
  };

  if (error) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white shadow rounded-lg p-8">
          <div className="text-center">
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={() => navigate('/financial-input')}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            >
              Start Over
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!impact) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white shadow rounded-lg p-8">
          <div className="text-center">
            <p className="text-gray-600">Loading results...</p>
          </div>
        </div>
      </div>
    );
  }

  const runwayDelta = impact.runway_delta_months;
  const isPositive = runwayDelta > 0;

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white shadow rounded-lg p-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Hiring Impact Analysis
          </h2>
          <div className={`inline-flex items-center px-6 py-3 rounded-full text-lg font-semibold ${getRiskColor(impact.risk_level)}`}>
            <span className="mr-2 text-2xl">{getRiskEmoji(impact.risk_level)}</span>
            {impact.risk_level}
          </div>
        </div>

        <div className="space-y-6">
          {/* Main Impact Card */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              {getRiskMessage(impact.risk_level, impact.new_runway_months)}
            </h3>
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <p className="text-sm text-gray-600">Current Runway</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatMonths(impact.current_runway_months)}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">New Runway</p>
                <p className={`text-2xl font-bold ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                  {formatMonths(impact.new_runway_months)}
                </p>
              </div>
            </div>
          </div>

          {/* Runway Change */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Runway Change
            </h3>
            <div className="flex items-center">
              <div className={`text-3xl font-bold ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {isPositive ? '+' : ''}{Math.abs(impact.runway_delta_months).toFixed(1)} months
              </div>
              <p className="ml-4 text-gray-600">
                {isPositive
                  ? 'Your runway will increase'
                  : `Your runway will shorten by ${Math.abs(impact.runway_delta_months).toFixed(1)} months`}
              </p>
            </div>
          </div>

          {/* Financial Details */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Financial Impact
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Current monthly burn</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(Math.abs(impact.current_monthly_burn))}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">New monthly burn</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(Math.abs(impact.new_monthly_burn))}
                </span>
              </div>
              <div className="flex justify-between items-center pt-2 border-t">
                <span className="text-gray-600">Additional monthly cost</span>
                <span className="font-semibold text-red-600">
                  +{formatCurrency(Math.abs(impact.burn_delta))}
                </span>
              </div>
            </div>
          </div>

          {/* Hire Details */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Hire Details
            </h3>
            <div className="space-y-2">
              <p className="text-gray-600">
                <span className="font-medium">Role:</span> {impact.hire_scenario.role_title}
              </p>
              <p className="text-gray-600">
                <span className="font-medium">Total monthly cost:</span>{' '}
                {formatCurrency(
                  impact.hire_scenario.monthly_salary +
                  impact.hire_scenario.monthly_benefits +
                  impact.hire_scenario.monthly_overhead
                )}
              </p>
            </div>
          </div>

          {/* Actions */}
          <div className="border-t pt-6 flex gap-4">
            <button
              onClick={() => navigate('/hiring-input')}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Try Another Hire
            </button>
            <button
              onClick={() => navigate('/financial-input')}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Update Finances
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}


