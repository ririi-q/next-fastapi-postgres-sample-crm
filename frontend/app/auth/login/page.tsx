'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { LoginForm } from "@/components/login-form"
import { useNavigation } from '@/hooks/useNavigation';

export default function LoginPage() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const { navigateTo } = useNavigation();

  const handleLogin = async (email: string, password: string) => {
    try {
      const response = await fetch('http://localhost:5000/api/v1/auth/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'username': email,
          'password': password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        login(data.access_token, data.refresh_token);
        navigateTo('/');
      } else {
        setError('ログインに失敗しました。');
      }
    } catch (error) {
      console.error('ログインエラー:', error);
      setError('ログイン中にエラーが発生しました。');
    }
  };

  const handleGoogleLogin = async () => {
    try {
      window.location.href = 'http://localhost:5000/api/v1/auth/google-oauth2/authorize';
    } catch (error) {
      console.error('Googleログインエラー:', error);
      setError('Googleログイン中にエラーが発生しました。');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <LoginForm onSubmit={handleLogin} onGoogleLogin={handleGoogleLogin} error={error} />
    </div>
  )
}
