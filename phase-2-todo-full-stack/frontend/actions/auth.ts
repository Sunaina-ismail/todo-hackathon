'use server';

import { redirect } from 'next/navigation';
import { headers } from 'next/headers';
import { auth } from '@/lib/auth';

type ActionResult = { error?: string } | { success: boolean };

/**
 * Sign up a new user
 */
export async function signUpAction(formData: FormData): Promise<ActionResult> {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  const confirmPassword = formData.get('confirmPassword') as string;

  // Validate passwords match
  if (password !== confirmPassword) {
    return { error: 'Passwords do not match' };
  }

  // Validate password length
  if (password.length < 8) {
    return { error: 'Password must be at least 8 characters' };
  }

  // Validate email
  if (!email || !email.includes('@')) {
    return { error: 'Please enter a valid email address' };
  }

  try {
    // Call Better Auth signUpEmail
    const response = await auth.api.signUpEmail({
      body: {
        email,
        password,
        name: email.split('@')[0] || email,
      },
      headers: await headers(),
    });
    console.log('[Auth] SignUp response:', JSON.stringify(response, null, 2));

    // Return success - client will handle redirect
    return { success: true };
  } catch (error: unknown) {
    // Handle Better Auth errors
    if (error && typeof error === 'object' && 'message' in error) {
      const authError = error as { message: string };

      // Check for common error messages
      if (authError.message.includes('already registered') || authError.message.includes('409')) {
        return { error: 'An account with this email already exists' };
      }
      if (authError.message.includes('validation') || authError.message.includes('400')) {
        return { error: 'Please check your input and try again' };
      }

      return { error: authError.message };
    }

    return { error: 'An unexpected error occurred. Please try again.' };
  }
}

/**
 * Sign in an existing user
 */
export async function signInAction(formData: FormData): Promise<ActionResult> {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;

  // Validate input
  if (!email || !password) {
    return { error: 'Please enter both email and password' };
  }

  if (!email.includes('@')) {
    return { error: 'Please enter a valid email address' };
  }

  try {
    // Call Better Auth signInEmail
    const response = await auth.api.signInEmail({
      body: {
        email,
        password,
      },
      headers: await headers(),
    });
    console.log('[Auth] SignIn response:', JSON.stringify(response, null, 2));

    // Return success - client will handle redirect
    return { success: true };
  } catch (error: unknown) {
    // Handle Better Auth errors
    if (error && typeof error === 'object' && 'message' in error) {
      const authError = error as { message: string };

      // Check for common error messages
      if (authError.message.includes('invalid') || authError.message.includes('401')) {
        return { error: 'Invalid email or password' };
      }
      if (authError.message.includes('validation') || authError.message.includes('400')) {
        return { error: 'Please check your input and try again' };
      }

      return { error: authError.message };
    }

    return { error: 'An unexpected error occurred. Please try again.' };
  }
}

/**
 * Sign out the current user
 */
export async function signOutAction() {
  try {
    await auth.api.signOut({
      headers: await headers(),
    });
    // Redirect to home page (which will redirect to sign-in)
    redirect('/');
  } catch (error) {
    console.error('Sign out error:', error);
    // Even if signOut fails, redirect to home
    redirect('/');
  }
}
