import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';
import { User } from '../types';
import { authService } from '../services/authService';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  token: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.login(email, password);
      const { access_token } = response;
      
      // Store token in localStorage
      localStorage.setItem('token', access_token);
      
      // Get user info
      const userInfo = await authService.getCurrentUser();
      
      set({
        isAuthenticated: true,
        user: userInfo,
        token: access_token,
        isLoading: false,
      });
    } catch (error) {
      console.error('Login error:', error);
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to login',
      });
    }
  },

  register: async (name, email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authService.register(name, email, password);
      
      // Auto login after successful registration
      await get().login(email, password);
      
      set({ isLoading: false });
    } catch (error) {
      console.error('Registration error:', error);
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to register',
      });
    }
  },

  logout: () => {
    // Clear token from localStorage
    localStorage.removeItem('token');
    
    set({
      user: null,
      isAuthenticated: false,
      token: null,
    });
  },

  checkAuth: async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      return;
    }
    
    // Check if token is expired
    try {
      const decodedToken: any = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      
      if (decodedToken.exp && decodedToken.exp < currentTime) {
        // Token expired
        get().logout();
        return;
      }
      
      // Token valid, get current user info
      const userInfo = await authService.getCurrentUser();
      
      set({
        isAuthenticated: true,
        user: userInfo,
        token,
      });
    } catch (error) {
      console.error('Token validation error:', error);
      get().logout();
    }
  },
}));