'use client';

import React, { createContext, useState, useContext, useEffect } from 'react';
import { Skeleton } from '@/components/ui/skeleton';
import { useNavigation } from '@/hooks/useNavigation';

interface AuthContextType {
  isAuthenticated: boolean | null;
  login: (token: string, refreshToken: string) => void;
  logout: () => void;
  refreshAccessToken: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const { navigateTo } = useNavigation();

  useEffect(() => {
    const checkAuth = async () => {
      await checkAuthStatus();
    };
    checkAuth();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('token');
      const refreshToken = localStorage.getItem('refreshToken');
      if (!token || !refreshToken) {
        setIsAuthenticated(false);
        return;
      }
      const response = await fetch('http://localhost:5000/api/v1/auth/check-auth', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        setIsAuthenticated(true);
      } else {
        const refreshed = await refreshAccessToken();
        setIsAuthenticated(refreshed);
      }
    } catch (error) {
      console.error('認証チェックエラー:', error);
      setIsAuthenticated(false);
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
    }
  };

  const login = (token: string, refreshToken: string) => {
    localStorage.setItem('token', token);
    localStorage.setItem('refreshToken', refreshToken);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    setIsAuthenticated(false);
    navigateTo('/auth/login');
  };

  const refreshAccessToken = async (): Promise<boolean> => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) return false;

    try {
      const response = await fetch('http://localhost:5000/api/v1/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        return true;
      } else {
        logout();
        return false;
      }
    } catch (error) {
      console.error('トークン更新エラー:', error);
      logout();
      return false;
    }
  };

  if (isAuthenticated === null) {
    return <Skeleton className="w-full h-full" />;
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout, refreshAccessToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
