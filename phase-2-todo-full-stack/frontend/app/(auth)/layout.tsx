import { getSession } from '@/lib/auth-client';
import { redirect } from 'next/navigation';

export default async function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Check if user is already authenticated
  const session = await getSession();

  const isAuthenticated = session &&
    typeof session === 'object' &&
    'data' in session &&
    session.data &&
    typeof session.data === 'object' &&
    'session' in session.data &&
    session.data.session;

  // Redirect authenticated users to dashboard
  if (isAuthenticated) {
    redirect('/dashboard');
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md">
        {children}
      </div>
    </div>
  );
}
