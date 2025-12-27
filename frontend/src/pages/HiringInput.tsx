import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { companyAPI, hireScenarioAPI, hiringImpactAPI } from '../api/client';

export default function HiringInput() {
  const navigate = useNavigate();
  const [companyId, setCompanyId] = useState<number | null>(null);
  const [roleTitle, setRoleTitle] = useState('');
  const [monthlySalary, setMonthlySalary] = useState('');
  const [monthlyBenefits, setMonthlyBenefits] = useState('');
  const [monthlyOverhead, setMonthlyOverhead] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCompany();
  }, []);

  const loadCompany = async () => {
    try {
      const companies = await companyAPI.list();
      if (companies.length > 0) {
        setCompanyId(companies[0].id);
      }
    } catch (err) {
      setError('Please complete the financial information first');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!companyId) {
        setError('Company not found. Please go back and complete financial information.');
        setLoading(false);
        return;
      }

      const financialSnapshotId = localStorage.getItem('financialSnapshotId');
      if (!financialSnapshotId) {
        setError('Financial information not found. Please go back and complete it first.');
        setLoading(false);
        return;
      }

      // Create hire scenario
      const scenario = await hireScenarioAPI.create(companyId, {
        role_title: roleTitle,
        monthly_salary: parseFloat(monthlySalary),
        monthly_benefits: parseFloat(monthlyBenefits),
        monthly_overhead: parseFloat(monthlyOverhead),
        start_date: new Date().toISOString(),
      });

      // Calculate hiring impact
      const impact = await hiringImpactAPI.calculate(
        parseInt(financialSnapshotId),
        scenario.id
      );

      // Store results for display
      localStorage.setItem('hiringImpact', JSON.stringify(impact));

      // Navigate to results
      navigate('/results');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to calculate hiring impact. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white shadow rounded-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Tell us about the person you're thinking of hiring
        </h2>
        <p className="text-gray-600 mb-6">
          We'll calculate how this hire affects your runway.
        </p>

        {error && (
          <div className="mb-6 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="roleTitle" className="block text-sm font-medium text-gray-700 mb-2">
              What role are you hiring for?
            </label>
            <input
              id="roleTitle"
              type="text"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="e.g., Senior Engineer, Sales Manager"
              value={roleTitle}
              onChange={(e) => setRoleTitle(e.target.value)}
            />
          </div>

          <div>
            <label htmlFor="monthlySalary" className="block text-sm font-medium text-gray-700 mb-2">
              Monthly salary
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500">$</span>
              <input
                id="monthlySalary"
                type="number"
                step="0.01"
                min="0"
                required
                className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="0.00"
                value={monthlySalary}
                onChange={(e) => setMonthlySalary(e.target.value)}
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">Base monthly salary</p>
          </div>

          <div>
            <label htmlFor="monthlyBenefits" className="block text-sm font-medium text-gray-700 mb-2">
              Monthly benefits cost
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500">$</span>
              <input
                id="monthlyBenefits"
                type="number"
                step="0.01"
                min="0"
                required
                className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="0.00"
                value={monthlyBenefits}
                onChange={(e) => setMonthlyBenefits(e.target.value)}
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">Health insurance, 401k, etc. (monthly average)</p>
          </div>

          <div>
            <label htmlFor="monthlyOverhead" className="block text-sm font-medium text-gray-700 mb-2">
              Monthly overhead
            </label>
            <div className="relative">
              <span className="absolute left-3 top-2 text-gray-500">$</span>
              <input
                id="monthlyOverhead"
                type="number"
                step="0.01"
                min="0"
                required
                className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="0.00"
                value={monthlyOverhead}
                onChange={(e) => setMonthlyOverhead(e.target.value)}
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">Equipment, software, office space (monthly average)</p>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Calculating...' : 'See the Impact'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}


