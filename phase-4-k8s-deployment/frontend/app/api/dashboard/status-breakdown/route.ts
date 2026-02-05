import { NextResponse } from 'next/server'
import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import jwt from 'jsonwebtoken'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

export async function GET() {
  try {
    // Get authenticated session
    const session = await auth.api.getSession({
      headers: await headers(),
    })

    if (!session?.user) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'UNAUTHORIZED',
            message: 'Authentication required'
          }
        },
        { status: 401 }
      )
    }

    // Get shared secret for JWT signing
    const API_JWT_SECRET = process.env.BETTER_AUTH_SECRET
    if (!API_JWT_SECRET) {
      console.error('BETTER_AUTH_SECRET not configured')
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INTERNAL_ERROR',
            message: 'Server configuration error'
          }
        },
        { status: 500 }
      )
    }

    // Mint a JWT token for FastAPI backend
    const claims = {
      sub: String(session.user.id),
      email: session.user.email,
      name: session.user.name,
    }

    const token = jwt.sign(claims, API_JWT_SECRET, {
      algorithm: 'HS256',
      expiresIn: '15m',
      issuer: 'nextjs-frontend',
      audience: 'fastapi-backend',
    })

    const userId = session.user.id

    // Fetch all tasks from backend (correct route with user ID)
    // Note: Backend has max limit of 100
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks?limit=100`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error('Failed to fetch tasks from backend')
    }

    const responseData = await response.json()
    // Backend returns nested structure: { data: { tasks: [...], total, limit, offset } }
    const tasks = responseData.data?.tasks || []

    const completedCount = tasks.filter((t: any) => t.completed).length
    const pendingCount = tasks.filter((t: any) => !t.completed).length
    const total = tasks.length

    const chartData = [
      {
        category: 'completed',
        value: completedCount,
        label: 'Completed',
        percentage: total > 0 ? (completedCount / total) * 100 : 0,
        color: '#BEF264'
      },
      {
        category: 'pending',
        value: pendingCount,
        label: 'Pending',
        percentage: total > 0 ? (pendingCount / total) * 100 : 0,
        color: '#1A221E'
      }
    ]

    return NextResponse.json({
      success: true,
      data: chartData
    })
  } catch (error) {
    console.error('Error fetching status breakdown:', error)
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_ERROR',
          message: 'Failed to fetch status breakdown'
        }
      },
      { status: 500 }
    )
  }
}
