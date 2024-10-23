'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useNavigation } from '@/hooks/useNavigation';
import { ClientLayout } from './client-layout';

interface UserData {
  name: string;
}

export default function Home() {
  const { isAuthenticated } = useAuth();
  const { navigateTo } = useNavigation();
  const [userData, setUserData] = useState<UserData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      navigateTo('/auth/login');
    } else if (!userData) {
      fetchUserData();
    }
    setIsLoading(false);
  }, [isAuthenticated, navigateTo, userData]);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUserData(data);
      } else {
        console.error('ユーザーデータの取得に失敗しました:', response.status);
      }
    } catch (error) {
      console.error('ユーザーデータの取得に失敗しました:', error);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <ClientLayout userData={userData}>
        <h1 className="text-2xl font-bold">Hello World!</h1>
    </ClientLayout>
  );
}