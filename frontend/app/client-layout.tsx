'use client';

import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"

interface UserData {
  name: string;
}

interface ClientLayoutProps {
  children: React.ReactNode;
  userData: UserData | null;
}

export function ClientLayout({ children, userData }: ClientLayoutProps) {
  return (
    <SidebarProvider>
      <AppSidebar userData={userData} />
      <main>
        <SidebarTrigger />
        {children}
      </main>
    </SidebarProvider>
  )
}
