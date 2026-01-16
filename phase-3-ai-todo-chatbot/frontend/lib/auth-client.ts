import { createAuthClient } from 'better-auth/react';

// Auto-detect URL based on environment
const getBaseURL = (): string => {
  // Priority 1: Explicit environment variable
  if (typeof process !== "undefined" && process.env.NEXT_PUBLIC_APP_URL) {
    return process.env.NEXT_PUBLIC_APP_URL;
  }

  // Priority 2: Vercel's automatic URL (production)
  if (typeof process !== "undefined" && process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }

  // Priority 3: Browser-side: use current location
  if (typeof window !== "undefined") {
    return `${window.location.protocol}//${window.location.host}`;
  }

  // Priority 4: Fallback to localhost for development
  return "http://localhost:3000";
};

/**
 * Better Auth client configuration
 * Uses shared secret JWT approach for Phase 2
 *
 * For client-side authentication (components, hooks)
 */
export const authClient = createAuthClient({
  baseURL: getBaseURL(),
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

/**
 * Get JWT token for backend API authentication.
 *
 * Calls /api/auth/token which generates an HS256 JWT using BETTER_AUTH_SECRET.
 * This token is compatible with the FastAPI backend's jwt.py verification.
 *
 * @returns Promise<{data?: {token: string}, error?: any}>
 */
export async function getToken(): Promise<{ data?: { token: string }; error?: unknown }> {
  try {
    const baseUrl = getBaseURL();
    const response = await fetch(`${baseUrl}/api/auth/token`, {
      method: 'GET',
      credentials: 'include', // Include cookies for session
    });

    if (!response.ok) {
      const error = await response.json();
      return { error };
    }

    const result = await response.json();
    return { data: result.data };
  } catch (error) {
    return { error };
  }
}
