/**
 * User session from Better Auth
 */
export interface UserSession {
  /** User ID (UUID) */
  id: string;
  /** User email */
  email: string;
  /** Session token */
  token: string;
  /** Session expiration */
  expires_at: Date;
}

/**
 * Sign-up form data
 */
export interface SignUpForm {
  /** User email address */
  email: string;
  /** User password (min 8 characters) */
  password: string;
  /** Password confirmation */
  confirmPassword: string;
}

/**
 * Sign-in form data
 */
export interface SignInForm {
  /** User email address */
  email: string;
  /** User password */
  password: string;
}
