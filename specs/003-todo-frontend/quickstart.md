# Quick Start Guide: Next.js 16 Todo Frontend

**Feature**: Next.js 16 Todo Frontend
**Date**: 2025-12-30
**Prerequisites**: FastAPI backend running, Node.js 18+

---

## Prerequisites

Before starting, ensure you have:

1. **Node.js 18+** (LTS recommended)
   ```bash
   node --version  # Should be 18.x or higher
   ```

2. **Package manager**: npm, yarn, or pnpm installed

3. **FastAPI backend running** at http://localhost:8000
   ```bash
   cd phase-2-todo-full-stack/backend
   uvicorn main:app --reload
   ```

4. **BETTER_AUTH_SECRET** from your backend `.env` file

---

## Installation

### 1. Navigate to Frontend Directory

```bash
cd phase-2-todo-full-stack/frontend
```

### 2. Install Dependencies

```bash
# Using npm
npm install

# Or using yarn
yarn install

# Or using pnpm
pnpm install
```

### 3. Environment Setup

Create `.env.local` in the frontend root directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-shared-secret-from-backend-env
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Important**: The `BETTER_AUTH_SECRET` must match the value in your backend's `.env` file for JWT validation to work.

---

## Development

### Start Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

### Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run type-check` | Run TypeScript type checking |
| `npm run test` | Run test suite |
| `npm run test:watch` | Run tests in watch mode |

---

## Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth route group
│   │   ├── sign-in/
│   │   └── sign-up/
│   ├── dashboard/           # Protected routes
│   ├── api/auth/[...all]/   # Better Auth API handler
│   ├── layout.tsx
│   └── page.tsx
├── actions/                  # Server Actions
│   ├── auth.ts
│   └── tasks.ts
├── components/               # React components
│   ├── auth/
│   ├── dashboard/
│   ├── tasks/
│   ├── layout/
│   └── ui/                   # Shadcn UI components
├── lib/                      # Utilities
│   ├── api-client.ts
│   ├── auth-client.ts
│   └── utils.ts
├── types/                    # TypeScript types
│   ├── api.ts
│   ├── task.ts
│   └── auth.ts
├── .env.local               # Environment variables
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

---

## First Run Verification

1. **Start the backend** (in one terminal):
   ```bash
   cd phase-2-todo-full-stack/backend
   uvicorn main:app --reload
   ```

2. **Start the frontend** (in another terminal):
   ```bash
   cd phase-2-todo-full-stack/frontend
   npm run dev
   ```

3. **Visit http://localhost:3000**

4. **Expected behavior**:
   - You should see the home page
   - Click "Sign Up" to create an account
   - After sign-up, you should be redirected to the dashboard
   - Dashboard should show empty state (no tasks yet)

---

## Building for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

### Production Environment Variables

For production, set these environment variables:

```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com
BETTER_AUTH_SECRET=<same-secret-as-backend>
BETTER_AUTH_URL=https://your-frontend-domain.com
NEXT_PUBLIC_APP_URL=https://your-frontend-domain.com
```

---

## Troubleshooting

### "BETTER_AUTH_SECRET is required" error

Ensure your `.env.local` file has the `BETTER_AUTH_SECRET` variable that matches your backend's secret.

### CORS errors

Verify your FastAPI backend has CORS configured to allow requests from `http://localhost:3000`.

### TypeScript errors

Run type checking to see all errors:
```bash
npm run type-check
```

### Cannot connect to backend

Check that:
1. Backend is running (`uvicorn main:app --reload`)
2. `NEXT_PUBLIC_API_URL` points to correct backend URL
3. No firewall blocking the connection

---

## Related Documentation

- [Spec](./spec.md) - Feature specification
- [Plan](./plan.md) - Implementation plan
- [Data Model](./data-model.md) - Type definitions
- [Reference Code](../reference-code-uneeza/) - Project pattern reference
