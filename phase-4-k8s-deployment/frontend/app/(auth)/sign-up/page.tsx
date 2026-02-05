import Link from 'next/link';
import { SignUpForm } from '@/components/auth/sign-up-form';

// Force dynamic rendering to avoid static generation
export const dynamic = 'force-dynamic';

export default function SignUpPage() {
  return (
    <div className="w-full max-w-md space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-2xl font-bold tracking-tight text-white">Create an account</h1>
        <p className="text-sm text-forest-gray">
          Enter your details below to create your account
        </p>
      </div>

      {/* Sign Up Form */}
      <SignUpForm />

      {/* Sign In Link */}
      <p className="text-center text-sm text-forest-gray">
        Already have an account?{' '}
        <Link
          href="/sign-in"
          className="font-medium text-neon-lime hover:text-neon-lime/80 transition-colors"
        >
          Sign in
        </Link>
      </p>
    </div>
  );
}
