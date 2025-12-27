/**
 * API Client for AXIOM Backend
 * 
 * Handles all API communication with the FastAPI backend.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors (unauthorized)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types
export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
}

export interface Company {
  id: number;
  name: string;
  user_id: number;
  created_at: string;
}

export interface FinancialSnapshot {
  id: number;
  company_id: number;
  current_cash: number;
  monthly_revenue: number;
  monthly_expenses: number;
  snapshot_date: string;
  created_at: string;
}

export interface HireScenario {
  id: number;
  company_id: number;
  role_title: string;
  monthly_salary: number;
  monthly_benefits: number;
  monthly_overhead: number;
  start_date: string;
  created_at: string;
}

export interface HiringImpact {
  current_runway_months: number;
  new_runway_months: number;
  runway_delta_months: number;
  current_monthly_burn: number;
  new_monthly_burn: number;
  burn_delta: number;
  risk_level: 'Safe' | 'Risky' | 'Dangerous';
  financial_snapshot: FinancialSnapshot;
  hire_scenario: HireScenario;
}

// Auth API
export const authAPI = {
  register: async (email: string, name: string, password: string): Promise<User> => {
    const response = await apiClient.post('/auth/register', { email, name, password });
    return response.data;
  },

  login: async (email: string, password: string): Promise<{ access_token: string; token_type: string }> => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
};

// Company API
export const companyAPI = {
  create: async (name: string): Promise<Company> => {
    const response = await apiClient.post('/companies', { name });
    return response.data;
  },

  list: async (): Promise<Company[]> => {
    const response = await apiClient.get('/companies');
    return response.data;
  },

  get: async (id: number): Promise<Company> => {
    const response = await apiClient.get(`/companies/${id}`);
    return response.data;
  },
};

// Financial Snapshot API
export const financialSnapshotAPI = {
  create: async (
    companyId: number,
    data: {
      current_cash: number;
      monthly_revenue: number;
      monthly_expenses: number;
      snapshot_date: string;
    }
  ): Promise<FinancialSnapshot> => {
    const response = await apiClient.post(`/financial-snapshots?company_id=${companyId}`, data);
    return response.data;
  },

  list: async (companyId: number): Promise<FinancialSnapshot[]> => {
    const response = await apiClient.get(`/financial-snapshots?company_id=${companyId}`);
    return response.data;
  },

  get: async (id: number): Promise<FinancialSnapshot> => {
    const response = await apiClient.get(`/financial-snapshots/${id}`);
    return response.data;
  },
};

// Hire Scenario API
export const hireScenarioAPI = {
  create: async (
    companyId: number,
    data: {
      role_title: string;
      monthly_salary: number;
      monthly_benefits: number;
      monthly_overhead: number;
      start_date: string;
    }
  ): Promise<HireScenario> => {
    const response = await apiClient.post(`/hire-scenarios?company_id=${companyId}`, data);
    return response.data;
  },

  list: async (companyId: number): Promise<HireScenario[]> => {
    const response = await apiClient.get(`/hire-scenarios?company_id=${companyId}`);
    return response.data;
  },

  get: async (id: number): Promise<HireScenario> => {
    const response = await apiClient.get(`/hire-scenarios/${id}`);
    return response.data;
  },
};

// Hiring Impact API
export const hiringImpactAPI = {
  calculate: async (financialSnapshotId: number, hireScenarioId: number): Promise<HiringImpact> => {
    const response = await apiClient.post('/hiring-impact/calculate', {
      financial_snapshot_id: financialSnapshotId,
      hire_scenario_id: hireScenarioId,
    });
    return response.data;
  },
};

export default apiClient;


