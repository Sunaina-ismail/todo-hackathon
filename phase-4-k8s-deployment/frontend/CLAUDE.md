# Frontend - Phase 4 Kubernetes Deployment

## Overview
Next.js 16 (App Router) frontend deployed to Kubernetes using Docker standalone build with Helm chart management.

## Tech Stack
- **Framework:** Next.js 16.1.2 (App Router, Standalone Output)
- **Language:** TypeScript 5.x (Strict)
- **Auth:** Better Auth (JWT Strategy)
- **UI:** Tailwind CSS + Shadcn UI
- **AI Chat:** OpenAI ChatKit (@openai/chatkit-react)
- **Database:** Neon (Drizzle ORM for Auth tables ONLY)
- **Deployment:** Docker + Kubernetes + Helm

## Critical Kubernetes Fixes

### 1. ChatKit Proxy Route Handler
**Problem:** Next.js rewrites don't work for external URL proxying in standalone/Docker builds.

**Solution:** Created `/app/api/chatkit/route.ts` to manually proxy ChatKit requests to backend.

```typescript
// frontend/app/api/chatkit/route.ts
export async function POST(request: NextRequest) {
  const authHeader = request.headers.get('authorization');
  const body = await request.text();
  const backendUrl = `${BACKEND_URL}/api/chatkit`;

  const backendResponse = await fetch(backendUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': authHeader,
    },
    body: body,
  });

  // Stream SSE response back to client
  return new Response(backendResponse.body, {
    status: 200,
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

**Why:** In development mode (`npm run dev`), Next.js rewrites work. In Docker/Kubernetes with standalone builds, rewrites fail silently with 500 errors. The proxy route handler ensures ChatKit requests reach the backend.

### 2. Better Auth Localhost Configuration
**Problem:** Better Auth rejects requests from `http://localhost:3000` when accessed via port-forward.

**Solution:** Added localhost to trusted origins in `lib/auth.ts`:

```typescript
trustedOrigins: [
  ...(process.env.NEXT_PUBLIC_APP_URL ? [process.env.NEXT_PUBLIC_APP_URL] : []),
  'http://localhost:3000',
  'http://127.0.0.1:3000',
],
```

**Why:** When accessing via `kubectl port-forward`, browser sends requests from localhost, but Better Auth expects internal Kubernetes service URLs. Adding localhost to trusted origins allows authentication to work.

### 3. Next.js Rewrites Configuration
**Purpose:** Proxy task API and ChatKit endpoints to backend (works in dev, supplemented by route handler in production).

```typescript
// next.config.ts
const BACKEND_URL = process.env.BACKEND_URL ||
  (process.env.NODE_ENV === 'production'
    ? 'http://todo-app-backend:8001'
    : 'http://localhost:8001');

async rewrites() {
  return [
    {
      source: '/api/:userId/tasks/:path*',
      destination: `${BACKEND_URL}/api/:userId/tasks/:path*`,
    },
    {
      source: '/api/chatkit',
      destination: `${BACKEND_URL}/api/chatkit`,
    },
  ];
}
```

## Docker Configuration

### Multi-Stage Dockerfile
```dockerfile
# Stage 1: Dependencies
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Stage 2: Builder
FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build-time environment variables (dummy values)
ENV DATABASE_URL="postgresql://dummy:dummy@localhost:5432/dummy?sslmode=require"
ENV BETTER_AUTH_SECRET="dummy-secret-for-build-only-min-32-chars"
ENV BETTER_AUTH_URL="http://localhost:3000"

RUN npm run build

# Stage 3: Runner
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

RUN mkdir -p /app/.next/cache && chown -R nextjs:nodejs /app/.next

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

## Kubernetes Configuration

### Deployment
- **Image:** `todo-frontend:latest` (built in Minikube Docker daemon)
- **Port:** 3000
- **Replicas:** 1
- **Security:** Non-root user (UID 1000)
- **Health Probes:** Liveness and readiness on `/api/health` and `/api/ready`

### Service
- **Type:** NodePort
- **Port:** 3000
- **NodePort:** 30300 (external access)

### Environment Variables
**From ConfigMap:**
- `BACKEND_URL`: `http://todo-app-backend:8001`
- `FRONTEND_URL`: `http://todo-app-frontend:3000`
- `BETTER_AUTH_URL`: `http://todo-app-frontend:3000`

**From Secrets:**
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT validation

## Access Methods

### Windows/WSL2 Port-Forwarding
```bash
# Frontend (keep running in separate terminal)
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0

# Access from Windows browser
http://localhost:3000
```

**Important:** Use `--address 0.0.0.0` for Windows/WSL2 access. Without it, port-forward only binds to WSL2 localhost and isn't accessible from Windows.

### Linux/Mac NodePort Access
```bash
# Get Minikube IP
minikube ip

# Access via NodePort
http://<minikube-ip>:30300
```

## Development vs Production

### Development (npm run dev)
- Next.js rewrites work for API proxying
- Hot reload enabled
- Environment variables from `.env.local`
- Direct backend connection

### Production (Docker/Kubernetes)
- Standalone build with optimized output
- ChatKit proxy route handler required
- Environment variables from ConfigMap/Secrets
- Internal Kubernetes service communication

## Common Issues

### Issue 1: ChatKit 500 Errors
**Symptom:** `POST http://localhost:3000/api/chatkit 500 (Internal Server Error)`

**Cause:** Missing ChatKit proxy route handler in standalone build.

**Solution:** Ensure `/app/api/chatkit/route.ts` exists and is included in Docker build.

### Issue 2: Better Auth 403 Forbidden
**Symptom:** `POST http://localhost:3000/api/auth/sign-up/email 403 (FORBIDDEN)`

**Cause:** Better Auth rejects localhost origin.

**Solution:** Add localhost to `trustedOrigins` in `lib/auth.ts`.

### Issue 3: Port-Forward Not Accessible from Windows
**Symptom:** `ERR_CONNECTION_REFUSED` when accessing from Windows browser.

**Cause:** Port-forward bound to WSL2 localhost only.

**Solution:** Use `--address 0.0.0.0` flag in kubectl port-forward command.

## Build and Deploy

### Build Docker Image
```bash
# Use Minikube Docker daemon
eval $(minikube docker-env)

# Build image
docker build -t todo-frontend:latest -f frontend/Dockerfile frontend/
```

### Deploy with Helm
```bash
# Deploy or upgrade
helm upgrade --install todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-dev.yaml \
  -n todo-app \
  --set secrets.DATABASE_URL="$DATABASE_URL" \
  --set secrets.BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET"
```

### Restart Deployment
```bash
# After code changes and rebuild
kubectl rollout restart deployment -n todo-app todo-app-frontend
```

## Monitoring

### Check Logs
```bash
# Follow logs
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f

# Check for errors
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend --tail=100 | grep -i error
```

### Check Pod Status
```bash
kubectl get pods -n todo-app
kubectl describe pod -n todo-app <pod-name>
```

## Key Files
- `app/api/chatkit/route.ts` - ChatKit proxy handler (critical for Kubernetes)
- `lib/auth.ts` - Better Auth configuration with localhost trusted origins
- `next.config.ts` - Next.js rewrites and backend URL configuration
- `Dockerfile` - Multi-stage Docker build with standalone output
- `components/chat/chatkit-widget.tsx` - ChatKit widget with JWT authentication

## Environment Variables

### Required at Build Time
- `DATABASE_URL` - Dummy value for Drizzle schema generation
- `BETTER_AUTH_SECRET` - Dummy value for Better Auth initialization
- `BETTER_AUTH_URL` - Dummy value for Better Auth configuration

### Required at Runtime
- `DATABASE_URL` - Real Neon PostgreSQL connection (from Secret)
- `BETTER_AUTH_SECRET` - Real shared secret (from Secret)
- `BACKEND_URL` - Backend service URL (from ConfigMap)
- `BETTER_AUTH_URL` - Frontend service URL (from ConfigMap)

### Optional
- `NEXT_PUBLIC_API_URL` - Not needed with rewrites/proxy
- `NEXT_PUBLIC_CHATKIT_URL` - Not needed with proxy route
