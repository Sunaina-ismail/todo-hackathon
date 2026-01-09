import Link from 'next/link';
import { SignInForm } from '@/components/auth/sign-in-form';

// Force dynamic rendering to avoid static generation
export const dynamic = 'force-dynamic';

export default function SignInPage() {
  return (
    <div className="w-full max-w-md space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-2xl font-bold tracking-tight">Welcome back</h1>
        <p className="text-sm text-gray-500">
          Enter your email below to sign in to your account
        </p>
      </div>

      {/* Sign In Form */}
      <SignInForm />

      {/* Sign Up Link */}
      <p className="text-center text-sm text-gray-500">
        Don't have an account?{' '}
        <Link
          href="/sign-up"
          className="font-medium text-primary hover:underline"
        >
          Sign up
        </Link>
      </p>
    </div>
  );
}
