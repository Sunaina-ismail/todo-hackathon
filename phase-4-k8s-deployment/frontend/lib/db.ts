/**
 * Drizzle Database Client
 *
 * This file creates a Drizzle ORM client instance connected to Neon PostgreSQL.
 * This client is ONLY used for Better Auth tables (user, session, account).
 *
 * IMPORTANT: Task data is NOT queried through this client.
 * All task operations go through Server Actions that call the FastAPI backend.
 *
 * NOTE: Using Neon Pool client for better reliability in Next.js API routes
 */

import { drizzle } from 'drizzle-orm/neon-serverless'
import { Pool } from '@neondatabase/serverless'
import * as schema from '@/db/schema'

if (!process.env.DATABASE_URL) {
  throw new Error(
    'DATABASE_URL environment variable is required for Drizzle client'
  )
}

// Create Neon Pool client with proper configuration
// Pool client is more reliable for Next.js API routes than HTTP client
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  // Increase connection timeout to handle database wake-up from sleep
  connectionTimeoutMillis: 30000,
  // Allow time for queries to complete
  idleTimeoutMillis: 30000,
  // Maximum number of clients in the pool
  max: 10,
})

// Create Drizzle client with schema
export const db = drizzle(pool, { schema })
