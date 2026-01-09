/**
 * Dashboard Layout
 *
 * Layout wrapper for dashboard pages with authentication check
 */

import { redirect } from 'next/navigation';
import { headers } from 'next/headers';
import { auth } from '@/lib/auth';
// import { Header } from '@/components/layout/header';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

/**
 * Dashboard Layout
 * Ensures user is authenticated before rendering dashboard pages
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
    <div className="min-h-screen bg-gray-50">
      {/* <Header /> */}
      <main className="container mx-auto py-6 px-4">
        {children}
      </main>
    </div>
  );
}
