# Next.js 16 Todo Frontend

Phase 2 Todo Application frontend built with Next.js 16, Better Auth, and Tailwind CSS.

## Features

- 🔐 **Authentication**: Better Auth with JWT (shared secret with FastAPI backend)
- ✅ **Task Management**: Create, read, update, delete tasks with full CRUD operations
- 🔍 **Search & Filter**: Search tasks, filter by priority/tags, sort, and paginate
- 🏷️ **Tag Management**: Tags with usage counts for organization
- 🎨 **Modern UI**: Shadcn UI components with Tailwind CSS
- 📱 **Responsive**: Mobile-first design (320px+ to 1200px+)
- ⚡ **Performance**: Optimized for fast load times and smooth interactions

## Prerequisites

- Node.js 18+ (LTS recommended)
- npm, yarn, or pnpm
- FastAPI backend running at http://localhost:8000
- `BETTER_AUTH_SECRET` from backend `.env` file

## Installation

```bash
# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local and set BETTER_AUTH_SECRET to match your backend
```

## Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-shared-secret-from-backend
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**IMPORTANT**: `BETTER_AUTH_SECRET` must match the value in your backend's `.env` file.

## Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Type check
npm run type-check
```

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
│   ├── filters.ts
│   └── auth.ts
├── .env.local               # Environment variables
├── next.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5.x (strict mode)
- **Authentication**: Better Auth v1.0.0 with JWT
- **Styling**: Tailwind CSS + Shadcn UI
- **UI Components**: Radix UI primitives
- **Icons**: Lucide React
- **Date Handling**: date-fns
- **API**: FastAPI backend at http://localhost:8000

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`. All API calls use JWT Bearer authentication:

```typescript
Authorization: Bearer <jwt_token>
```

### Endpoints

- **Auth**: POST `/api/auth/sign-up`, POST `/api/auth/sign-in`
- **Tasks**: GET/POST `/api/{user_id}/tasks`, PUT/DELETE `/api/{user_id}/tasks/{task_id}`, PATCH `/api/{user_id}/tasks/{task_id}/complete`
- **Tags**: GET `/api/{user_id}/tags`

See [API Contracts](../../specs/003-todo-frontend/contracts/api-contracts.md) for full documentation.

## Development Workflow

1. **Start Backend**: Ensure FastAPI backend is running on port 8000
2. **Start Frontend**: Run `npm run dev` to start Next.js on port 3000
3. **Sign Up**: Create a new account at http://localhost:3000/sign-up
4. **Use App**: Access dashboard and manage tasks

## User Stories Implemented

- ✅ **US1**: User Authentication (sign-up, sign-in, sign-out)
- ✅ **US2**: View Task List (with loading and error states)
- ✅ **US3**: Create Task (with all fields)
- ✅ **US4**: Toggle Task Completion
- ✅ **US5**: Edit Task
- ✅ **US6**: Delete Task (with confirmation)
- ✅ **US7**: Search and Filter Tasks (search, priority, tags, sort, pagination)
- ✅ **US8**: View Tags (with usage counts)

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

## Documentation

- [Specification](../../specs/003-todo-frontend/spec.md) - Feature requirements
- [Implementation Plan](../../specs/003-todo-frontend/plan.md) - Architecture decisions
- [Data Model](../../specs/003-todo-frontend/data-model.md) - TypeScript interfaces
- [API Contracts](../../specs/003-todo-frontend/contracts/api-contracts.md) - Backend API documentation
- [Quick Start Guide](../../specs/003-todo-frontend/quickstart.md) - Setup guide
- [Tasks](../../specs/003-todo-frontend/tasks.md) - Implementation tasks

## License

Private project
