'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { RegisterForm } from "@/components/register-form"
import { useNavigation } from '@/hooks/useNavigation';

export default function RegisterPage() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const { navigateTo } = useNavigation();

  const handleRegister = async (name: string, email: string, password: string) => {
    try {
      const response = await fetch('http://localhost:5000/api/v1/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email,
          password,
        }),
      });

      if (response.ok) {
        // const data = await response.json();
        // 登録成功後、自動的にログインします
        const loginResponse = await fetch('http://localhost:5000/api/v1/auth/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            'username': email,
            'password': password,
          }),
        });

        if (loginResponse.ok) {
          const loginData = await loginResponse.json();
          login(loginData.access_token, loginData.refresh_token);
          navigateTo('/');
        } else {
          setError('登録は成功しましたが、ログインに失敗しました。');
        }
      } else {
        setError('登録に失敗しました。');
      }
    } catch (error) {
      console.error('登録エラー:', error);
      setError('登録中にエラーが発生しました。');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <RegisterForm onSubmit={handleRegister} error={error} />
    </div>
  )
}
