import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
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

// Response interceptor for handling common errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Handle authentication errors (401)
    if (error.response?.status === 401 && !originalRequest._retry) {
      // Clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
      return Promise.reject(new Error('Session expired. Please login again.'));
    }
    
    // Get error message
    const errorMessage = error.response?.data?.message || error.message || 'An error occurred';
    
    return Promise.reject(new Error(errorMessage));
  }
);

// Generic request function
const request = async <T>(config: AxiosRequestConfig): Promise<T> => {
  try {
    const response: AxiosResponse<T> = await api(config);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.message || error.message);
    }
    throw error;
  }
};

// API functions
export const apiService = {
  get: <T>(url: string, params?: any): Promise<T> => 
    request<T>({ method: 'GET', url, params }),
    
  post: <T>(url: string, data?: any): Promise<T> => 
    request<T>({ method: 'POST', url, data }),
    
  put: <T>(url: string, data?: any): Promise<T> => 
    request<T>({ method: 'PUT', url, data }),
    
  patch: <T>(url: string, data?: any): Promise<T> => 
    request<T>({ method: 'PATCH', url, data }),
    
  delete: <T>(url: string): Promise<T> => 
    request<T>({ method: 'DELETE', url }),
};
