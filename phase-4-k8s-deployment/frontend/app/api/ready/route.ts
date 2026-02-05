import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const errors: string[] = [];
    const checks = {
      environment: 'ok' as 'ok' | 'failed',
      database: 'n/a' as 'ok' | 'failed' | 'n/a',
    };

    // Validate required environment variables
    const requiredEnvVars = ['DATABASE_URL', 'BETTER_AUTH_SECRET'];

    for (const envVar of requiredEnvVars) {
      if (!process.env[envVar]) {
        checks.environment = 'failed';
        errors.push(`Missing required environment variable: ${envVar}`);
      }
    }

    // If any checks failed, return 503
    if (errors.length > 0) {
      return NextResponse.json(
        {
          status: 'not_ready',
          timestamp: new Date().toISOString(),
          service: 'frontend',
          checks,
          errors,
        },
        { status: 503 }
      );
    }

    // All checks passed
    return NextResponse.json(
      {
        status: 'ready',
        timestamp: new Date().toISOString(),
        service: 'frontend',
        checks,
      },
      { status: 200 }
    );
  } catch (error) {
    return NextResponse.json(
      {
        status: 'not_ready',
        timestamp: new Date().toISOString(),
        service: 'frontend',
        checks: {
          environment: 'failed',
          database: 'n/a',
        },
        errors: ['Unexpected error during readiness check'],
      },
      { status: 503 }
    );
  }
}
