import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { companyAPI, financialSnapshotAPI } from '../api/client';

export default function FinancialInput() {
  const navigate = useNavigate();
  const [companyName, setCompanyName] = useState('');
  const [currentCash, setCurrentCash] = useState('');
  const [monthlyRevenue, setMonthlyRevenue] = useState('');
  const [monthlyExpenses, setMonthlyExpenses] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [companyId, setCompanyId] = useState<number | null>(null);

  useEffect(() => {
    // Check if company exists, if not we'll create one
    loadCompany();
  }, []);

  const loadCompany = async () => {
    try {
      const companies = await companyAPI.list();
      if (companies.length > 0) {
        setCompanyId(companies[0].id);
        setCompanyName(companies[0].name);
      }
    } catch (err) {
      // No company yet, that's okay
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let finalCompanyId = companyId;

      // Create company if it doesn't exist
      if (!finalCompanyId) {
        if (!companyName.trim()) {
          setError('Please enter your company name');
          setLoading(false);
          return;
        }
        const company = await companyAPI.create(companyName);
        finalCompanyId = company.id;
        setCompanyId(company.id);
      }

      // Create financial snapshot
      const snapshot = await financialSnapshotAPI.create(finalCompanyId, {
        current_cash: parseFloat(currentCash),
        monthly_revenue: parseFloat(monthlyRevenue),
        monthly_expenses: parseFloat(monthlyExpenses),
        snapshot_date: new Date().toISOString(),
      });

      // Store snapshot ID for next step
      localStorage.setItem('financialSnapshotId', snapshot.id.toString());

      // Navigate to hiring input
      navigate('/hiring-input');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save financial information. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white shadow rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Tell us about your company's finances
        </h2>
        <p className="text-gray-600 mb-6">
          We'll use this to calculate how long your runway will last.
        </p>

        {error && (
          <div className="mb-6 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {!companyId && (
            <div>
              <label htmlFor="companyName" className="block text-sm font-medium text-gray-700 mb-2">
                Company Name
              </label>
              <input
                id="companyName"
                type="text"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Your company name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
              />
            </div>
          )}

          <div>
            <label htmlFor="currentCash" className="block text-sm font-medium text-gray-700 mb-2">
              How much cash do you have right now?
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500">$</span>
              <input
                id="currentCash"
                type="number"
                step="0.01"
                min="0"
                required
                className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="0.00"
                value={currentCash}
                onChange={(e) => setCurrentCash(e.target.value)}
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">Your current bank balance</p>
          </div>

          <div>
            <label htmlFor="monthlyRevenue" className="block text-sm font-medium text-gray-700 mb-2">
              How much do you make per month?
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500">$</span>
              <input
                id="monthlyRevenue"
                type="number"
                step="0.01"
                min="0"
                required
                className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="0.00"
                value={monthlyRevenue}
                onChange={(e) => setMonthlyRevenue(e.target.value)}
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">Average monthly revenue</p>
          </div>

          <div>
            <label htmlFor="monthlyExpenses" className="block text-sm font-medium text-gray-700 mb-2">
              How much do you spend per month?
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500">$</span>
              <input
                id="monthlyExpenses"
                type="number"
                step="0.01"
                min="0"
                required
                className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="0.00"
                value={monthlyExpenses}
                onChange={(e) => setMonthlyExpenses(e.target.value)}
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">Total monthly expenses (salaries, rent, etc.)</p>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : 'Continue to Hiring Details'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}


