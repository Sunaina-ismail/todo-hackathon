/**
 * Dashboard Layout
 *
 * Layout wrapper for dashboard pages with authentication check
 * Includes sidebar navigation and global chat button
 */

import { redirect } from 'next/navigation';
import { headers } from 'next/headers';
import { auth } from '@/lib/auth';
import { DashboardLayout as DashboardLayoutComponent } from '@/components/layout/dashboard-layout';
import { GlobalChatButton } from '@/components/chat/global-chat-button';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

/**
 * Dashboard Layout
 * Ensures user is authenticated before rendering dashboard pages
 * Wraps content with sidebar and adds global chat button
 */
export default async function DashboardLayout({ children }: DashboardLayoutProps) {
  // Check authentication using server-side Better Auth
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  // Redirect to sign-in if not authenticated
  if (!session?.user) {
    redirect('/sign-in?callbackUrl=/dashboard');
  }

  return (
    <DashboardLayoutComponent>
      {/* Global Chat Button - appears on all dashboard pages */}
      <GlobalChatButton />

      {children}
    </DashboardLayoutComponent>
  );
}
