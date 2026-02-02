// File: app/dashboard/layout.tsx
import React from 'react';
import { SuperSearchProvider } from '@/components/providers/SuperSearchProvider';
import { WebSocketProvider } from '@/components/providers/WebSocketProvider';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <WebSocketProvider>
      <SuperSearchProvider>
        <div className="super-search-dashboard">
          {children}
        </div>
      </SuperSearchProvider>
    </WebSocketProvider>
  );
}