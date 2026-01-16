/**
 * API request configuration
 */
export interface APIRequestConfig extends RequestInit {
  /** Optional timeout in milliseconds */
  timeout?: number;
  /** Whether to include credentials (cookies) */
  credentials?: RequestCredentials;
}

/**
 * API error response
 */
export interface APIError {
  /** Error message */
  detail: string;
  /** HTTP status code */
  status?: number;
  /** Additional error context */
  context?: Record<string, unknown>;
}

/**
 * API client error class
 */
export class APIClientError extends Error {
  status: number;
  detail: string;
  context?: Record<string, unknown>;

  constructor(message: string, status: number, detail?: string, context?: Record<string, unknown>) {
    super(message);
    this.name = 'APIClientError';
    this.status = status;
    this.detail = detail || message;
    this.context = context;
  }
}

/**
 * Generic API response wrapper
 */
export interface APIResponse<T = unknown> {
  data?: T;
  error?: APIError;
  status: number;
}
