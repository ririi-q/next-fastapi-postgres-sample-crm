'use client';

import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export default function CallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();

  useEffect(() => {
    const token = searchParams.get('token');
    if (token) {
      login(token, token); // リフレッシュトークンの処理は省略
      router.push('/');
    } else {
      router.push('/auth/login');
    }
  }, [searchParams, login, router]);

  return <div>Processing login...</div>;
}

