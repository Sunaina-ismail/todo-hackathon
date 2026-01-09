import { createAuthClient } from 'better-auth/react';

/**
 * Better Auth client configuration
 * Uses shared secret JWT approach for Phase 2
 *
 * For client-side authentication (components, hooks)
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
});

/**
 * Export auth hooks and methods for use in components
 * These are the client-side APIs for authentication
 */
export const {
  useSession,
  signIn,
  signUp,
  signOut,
  getSession,
} = authClient;
