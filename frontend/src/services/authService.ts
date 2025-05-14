import { apiService } from './api';
import { AuthResponse, LoginCredentials, RegisterData, User } from '../types';

export const authService = {
  // Register a new user
  register: async (name: string, email: string, password: string): Promise<User> => {
    const data: RegisterData = {
      name,
      email,
      password,
    };
    return apiService.post<User>('/auth/register', data);
  },

  // Login user
  login: async (email: string, password: string): Promise<AuthResponse> => {
    const credentials: LoginCredentials = {
      email,
      password,
    };
    return apiService.post<AuthResponse>('/auth/login', credentials);
  },

  // Get current user profile
  getCurrentUser: async (): Promise<User> => {
    return apiService.get<User>('/auth/me');
  },
};