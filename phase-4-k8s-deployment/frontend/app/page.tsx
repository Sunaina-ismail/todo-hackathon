import { redirect } from 'next/navigation';
import { getSession } from '@/lib/auth-client';

// Force dynamic rendering to avoid static generation (uses getSession)
export const dynamic = 'force-dynamic';

export default async function HomePage() {
  // Check if user is authenticated
  const session = await getSession();

  // Type-safe extraction of session data
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

  // Redirect unauthenticated users to sign-in
  redirect('/sign-in');
}
