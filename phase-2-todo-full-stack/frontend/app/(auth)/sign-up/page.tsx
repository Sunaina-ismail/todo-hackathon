import Link from 'next/link';
import { SignUpForm } from '@/components/auth/sign-up-form';

// Force dynamic rendering to avoid static generation
export const dynamic = 'force-dynamic';

export default function SignUpPage() {
  return (
    <div className="w-full max-w-md space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-2xl font-bold tracking-tight">Create an account</h1>
        <p className="text-sm text-gray-500">
          Enter your details below to create your account
        </p>
      </div>

      {/* Sign Up Form */}
      <SignUpForm />

      {/* Sign In Link */}
      <p className="text-center text-sm text-gray-500">
        Already have an account?{' '}
        <Link
          href="/sign-in"
          className="font-medium text-primary hover:underline"
        >
          Sign in
        </Link>
      </p>
    </div>
  );
}
