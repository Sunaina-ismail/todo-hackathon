# JWT Minting in Server Actions - Production Pattern

## Overview

This document describes the **production-recommended** JWT minting pattern for Server Actions in Next.js 16 with Better Auth. This pattern provides better security than directly extracting session tokens.

## Why Mint a New JWT?

| Aspect | Direct Session Token | Minted JWT |
|--------|---------------------|------------|
| **Expiry** | 7 days (session duration) | 15 minutes |
| **Claims** | Fixed by Better Auth | Customizable |
| **Issuer/Audience** | Not validated | Validated |
| **Use Case** | Internal APIs | External APIs |

**Benefits of JWT Minting:**
- Short-lived tokens limit exposure if leaked
- Custom claims for backend needs
- Issuer/audience validation prevents token reuse
- Better separation of concerns

## Implementation

### 1. Server Action with JWT Minting

```typescript
// frontend/actions/tasks.ts
'use server'

import { revalidatePath } from 'next/cache'
import { headers } from 'next/headers'
import jwt from 'jsonwebtoken'
import type { Task, TaskCreate, TaskUpdate } from '@/types/task'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * Get authenticated user and mint JWT token for backend API
 * This runs on the server and has access to cookies
 */
async function getAuthenticatedUser(): Promise<{ userId: string; token: string } | null> {
  try {
    // Import Better Auth server instance
    const { auth } = await import('@/lib/auth')

    // Get session from cookies (Server API)
    const session = await auth.api.getSession({
      headers: await headers(),
    })

    if (!session?.user?.id) {
      return null
    }

    // Get the shared secret for JWT signing
    const API_JWT_SECRET = process.env.BETTER_AUTH_SECRET
    if (!API_JWT_SECRET) {
      console.error('BETTER_AUTH_SECRET not configured')
      return null
    }

    // Mint a JWT token for the FastAPI backend
    // This JWT is signed with the same secret the backend uses for verification
    const claims = {
      sub: String(session.user.id), // User ID as subject (required)
      email: session.user.email,    // Additional claims
      name: session.user.name,      // Additional claims
    }

    const token = jwt.sign(claims, API_JWT_SECRET, {
      algorithm: 'HS256',           // HS256 for shared secret
      expiresIn: '15m',             // Short-lived for security
      issuer: 'nextjs-frontend',    // Token issuer
      audience: 'fastapi-backend',  // Expected audience
    })

    return {
      userId: session.user.id,
      token,
    }
  } catch (error) {
    console.error('Failed to get authenticated user:', error)
    return null
  }
}

/**
 * Make authenticated API request to FastAPI backend
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<{ data?: T; error?: string }> {
  const auth = await getAuthenticatedUser()

  if (!auth) {
    return { error: 'Unauthorized - please sign in' }
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth.token}`,  // Minted JWT
        ...options.headers,
      },
    })

    // Handle 401 Unauthorized
    if (response.status === 401) {
      return { error: 'Session expired - please sign in again' }
    }

    // Handle other errors
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      return {
        error: errorData.detail || errorData.message || `Request failed with status ${response.status}`,
      }
    }

    // Parse JSON response
    const data = await response.json()
    return { data }
  } catch (error) {
    console.error('API request failed:', error)
    return {
      error: error instanceof Error ? error.message : 'Network error - unable to reach server',
    }
  }
}

/**
 * Fetch all tasks for the authenticated user
 */
export async function fetchTasks(params?: {
  status?: string
  limit?: number
  offset?: number
}): Promise<{ tasks?: Task[]; total?: number; error?: string }> {
  const auth = await getAuthenticatedUser()

  if (!auth) {
    return { error: 'Unauthorized - please sign in' }
  }

  const queryParams = new URLSearchParams()
  if (params?.status) queryParams.append('status', params.status)
  if (params?.limit) queryParams.append('limit', params.limit.toString())
  if (params?.offset) queryParams.append('offset', params.offset.toString())

  const queryString = queryParams.toString()
  const endpoint = `/api/${auth.userId}/tasks${queryString ? `?${queryString}` : ''}`

  const result = await apiRequest<{ tasks: Task[]; total: number }>(endpoint, {
    method: 'GET',
  })

  if (result.error) {
    return { error: result.error }
  }

  return {
    tasks: result.data?.tasks || [],
    total: result.data?.total || 0,
  }
}

/**
 * Create a new task
 */
export async function createTask(
  data: TaskCreate
): Promise<{ task?: Task; error?: string }> {
  const auth = await getAuthenticatedUser()

  if (!auth) {
    return { error: 'Unauthorized - please sign in' }
  }

  const endpoint = `/api/${auth.userId}/tasks`

  const result = await apiRequest<Task>(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  })

  if (result.error) {
    return { error: result.error }
  }

  revalidatePath('/dashboard')

  return { task: result.data }
}

/**
 * Update an existing task
 */
export async function updateTask(
  taskId: string,
  data: TaskUpdate
): Promise<{ task?: Task; error?: string }> {
  const auth = await getAuthenticatedUser()

  if (!auth) {
    return { error: 'Unauthorized - please sign in' }
  }

  const endpoint = `/api/${auth.userId}/tasks/${taskId}`

  const result = await apiRequest<Task>(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })

  if (result.error) {
    return { error: result.error }
  }

  revalidatePath('/dashboard')

  return { task: result.data }
}

/**
 * Delete a task
 */
export async function deleteTask(
  taskId: string
): Promise<{ success?: boolean; error?: string }> {
  const auth = await getAuthenticatedUser()

  if (!auth) {
    return { error: 'Unauthorized - please sign in' }
  }

  const endpoint = `/api/${auth.userId}/tasks/${taskId}`

  const result = await apiRequest<void>(endpoint, {
    method: 'DELETE',
  })

  if (result.error) {
    return { error: result.error }
  }

  revalidatePath('/dashboard')

  return { success: true }
}

/**
 * Toggle task completion status
 */
export async function toggleTaskComplete(
  taskId: string,
  currentCompleted: boolean
): Promise<{ task?: Task; error?: string }> {
  const auth = await getAuthenticatedUser()

  if (!auth) {
    return { error: 'Unauthorized - please sign in' }
  }

  const endpoint = `/api/${auth.userId}/tasks/${taskId}`

  const result = await apiRequest<Task>(endpoint, {
    method: 'PATCH',
    body: JSON.stringify({ completed: !currentCompleted }),
  })

  if (result.error) {
    return { error: result.error }
  }

  revalidatePath('/dashboard')

  return { task: result.data }
}
```

### 2. Backend JWT Validation with Issuer/Audience

```python
# backend/src/auth/jwt.py
from jose import jwt, JWTError
from typing import Dict, Any
from fastapi import HTTPException, status
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")

ALGORITHM = "HS256"

def verify_jwt(token: str) -> Dict[str, Any]:
    """
    Verify JWT token from Next.js frontend.

    Validates:
    - Signature using shared BETTER_AUTH_SECRET
    - Issuer is 'nextjs-frontend'
    - Audience is 'fastapi-backend'
    - Token not expired
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={
                "verify_iss": True,      # Verify issuer
                "verify_aud": True,      # Verify audience
                "require": ["sub"],       # Require 'sub' claim
            },
            issuer="nextjs-frontend",    # Expected issuer
            audience="fastapi-backend",  # Expected audience
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
```

## Environment Variables

```bash
# Frontend (.env.local)
BETTER_AUTH_SECRET=your-super-secret-key-here-minimum-32-characters
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (.env)
BETTER_AUTH_SECRET=your-super-secret-key-here-minimum-32-characters
```

**IMPORTANT:** Both services MUST use the same `BETTER_AUTH_SECRET`.

## JWT Claims Reference

| Claim | Type | Required | Description |
|-------|------|----------|-------------|
| `sub` | string | Yes | User ID (subject) |
| `email` | string | No | User's email |
| `name` | string | No | User's name |
| `iss` | string | Yes | Issuer (`nextjs-frontend`) |
| `aud` | string | Yes | Audience (`fastapi-backend`) |
| `exp` | number | Yes | Expiration timestamp |
| `iat` | number | Yes | Issued at timestamp |

## Security Best Practices

1. **Short Expiry**: Use `15m` for API JWTs to limit exposure
2. **Validate Issuer/Audience**: Backend should reject unknown tokens
3. **Same Secret**: Both services must use identical `BETTER_AUTH_SECRET`
4. **HTTPS Only**: Never transmit tokens over plain HTTP in production
5. **Log Failures**: Log authentication failures for debugging

## Comparison: Simple vs Production

### Simple Pattern (Skills Default)
- Direct session token extraction
- Works for internal APIs
- Less secure (long-lived tokens)

### Production Pattern (This Document)
- Mint new short-lived JWT
- Issuer/audience validation
- Better for external/fastapi backends

## When to Use Which

| Use Case | Pattern |
|----------|---------|
| Internal microservices | Simple pattern |
| External API consumers | Production pattern |
| High-security requirements | Production pattern |
| Quick prototyping | Simple pattern |
