/**
 * ChatKit API Proxy Route
 *
 * Proxies ChatKit requests from frontend to backend ChatKitServer.
 * Required for Docker/Kubernetes deployments because Next.js rewrites
 * don't work reliably for external URLs in standalone builds.
 *
 * Flow:
 * 1. Frontend ChatKit widget sends POST to /api/chatkit
 * 2. This route receives the request with JWT token in Authorization header
 * 3. Forwards request to backend at BACKEND_URL/api/chatkit
 * 4. Streams the SSE response back to the client
 */

import { NextRequest } from 'next/server';

// Get backend URL from environment or use default
const BACKEND_URL = process.env.BACKEND_URL || 'http://todo-app-backend:8001';

export async function POST(request: NextRequest) {
  try {
    // Get the Authorization header (JWT token)
    const authHeader = request.headers.get('authorization');

    if (!authHeader) {
      return new Response(
        JSON.stringify({ error: 'Missing authorization header' }),
        {
          status: 401,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }

    // Get the request body
    const body = await request.text();

    // Forward the request to the backend
    const backendUrl = `${BACKEND_URL}/api/chatkit`;

    console.log('[ChatKit Proxy] Forwarding request to:', backendUrl);

    const backendResponse = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authHeader,
      },
      body: body,
    });

    console.log('[ChatKit Proxy] Backend response status:', backendResponse.status);

    // If the backend returns an error, forward it
    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error('[ChatKit Proxy] Backend error:', errorText);
      return new Response(errorText, {
        status: backendResponse.status,
        headers: {
          'Content-Type': backendResponse.headers.get('Content-Type') || 'application/json',
        },
      });
    }

    // Check if the response is SSE (Server-Sent Events)
    const contentType = backendResponse.headers.get('Content-Type') || '';

    if (contentType.includes('text/event-stream')) {
      // Stream the SSE response back to the client
      console.log('[ChatKit Proxy] Streaming SSE response');

      return new Response(backendResponse.body, {
        status: 200,
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    } else {
      // Return regular JSON response
      const responseText = await backendResponse.text();
      return new Response(responseText, {
        status: backendResponse.status,
        headers: {
          'Content-Type': contentType,
        },
      });
    }
  } catch (error) {
    console.error('[ChatKit Proxy] Error:', error);
    return new Response(
      JSON.stringify({
        error: 'Failed to proxy request to backend',
        details: error instanceof Error ? error.message : String(error)
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
