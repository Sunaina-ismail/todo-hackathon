import type { NextConfig } from 'next'

// Backend URL - use Kubernetes service name for container deployment
// In local dev, use localhost:8001 (8000 is in use by another application)
const BACKEND_URL = process.env.BACKEND_URL ||
  (process.env.NODE_ENV === 'production'
    ? 'http://todo-app-backend:8001'
    : 'http://localhost:8001');

const nextConfig: NextConfig = {
  // Enable standalone output for Docker deployment
  output: 'standalone',

  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },

  async rewrites() {
    return [
      {
        // Proxy task API endpoints to backend
        source: '/api/:userId/tasks/:path*',
        destination: `${BACKEND_URL}/api/:userId/tasks/:path*`,
      },
      {
        // Proxy chatkit endpoint to backend
        source: '/api/chatkit',
        destination: `${BACKEND_URL}/api/chatkit`,
      },
      // Note: /api/auth/* endpoints are handled by frontend Better Auth
      // Do NOT proxy them to backend
    ];
  },
}

export default nextConfig
