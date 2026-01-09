# Implementation Plan: Next.js 16 Todo Frontend

**Branch**: `003-todo-frontend` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-todo-frontend/spec.md`

## Summary

Build a Next.js 16 frontend application with Better Auth integration for user authentication (sign-up, sign-in, sign-out), connected to the completed FastAPI backend at `phase-2-todo-full-stack/backend/`. Features include task CRUD operations with JWT shared secret authentication, search/filter/sort/pagination, and tag management with usage counts. Follows the reference-code-uneeza project structure using Shadcn UI components and Tailwind CSS styling.

## Technical Context

**Language/Version**: TypeScript 5.x (Next.js 16 requirement) | **Primary Dependencies**: Next.js 16 (App Router), Better Auth v1.0.0, Shadcn UI, Tailwind CSS, React 19.x, date-fns | **Storage**: N/A (frontend only - API calls to FastAPI backend) | **Testing**: Vitest + React Testing Library for component tests, Jest for integration tests | **Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge) | **Project Type**: Single web application (Next.js frontend) | **Performance Goals**: Task list loads within 2 seconds for 100 tasks, search/filter within 500ms | **Constraints**: Responsive design (320px+ mobile, 1200px+ desktop), JWT session persistence, httpOnly cookies | **Scale/Scope**: Single-user frontend connected to existing backend, no local database required

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Type Safety (tsc --strict) | ✅ PASS | TypeScript strict mode mandatory |
| Automated Testing | ✅ PASS | Frontend component tests required |
| Better Auth JWT Integration | ✅ PASS | Shared secret BETTER_AUTH_SECRET |
| Next.js 16+ App Router | ✅ PASS | Using App Router pattern |
| Tailwind CSS + Shadcn UI | ✅ PASS | Following reference-code-uneeza |
| No forbidden technologies | ✅ PASS | Uses only approved stack |

## Project Structure

### Documentation (this feature)

```text
specs/003-todo-frontend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (if needed)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-2-todo-full-stack/frontend/        # NEW - Next.js frontend (mirrors reference-code-uneeza structure)
├── app/                                  # Next.js App Router
│   ├── (auth)/                           # Auth route group
│   │   ├── sign-in/
│   │   └── sign-up/
│   ├── dashboard/                        # Protected routes (requires auth)
│   ├── api/auth/[...all]/                # Better Auth handler
│   ├── layout.tsx
│   └── page.tsx
├── actions/                              # Server Actions
│   ├── auth.ts                           # Auth actions
│   └── tasks.ts                          # Task CRUD actions
├── components/
│   ├── auth/                             # Auth forms (sign-in, sign-up)
│   ├── dashboard/                        # Dashboard UI
│   ├── tasks/                            # Task components (list, form, item)
│   ├── layout/                           # Header, sidebar, user menu
│   └── ui/                               # Shadcn UI components
├── lib/
│   ├── api-client.ts                     # API client with JWT attachment
│   ├── auth-client.ts                    # Better Auth client
│   └── utils.ts
├── types/
│   ├── api.ts                            # API request/response types
│   └── task.ts                           # Task types
├── .env.local                            # Environment variables
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

**Structure Decision**: Following reference-code-uneeza pattern with Next.js 16 App Router, using Server Actions for backend communication, and Shadcn UI for components. Frontend connects to existing FastAPI backend at `/phase-2-todo-full-stack/backend/`.

## Complexity Tracking

*No Constitution violations - all gates pass with approved technologies.*

---

## Phase 0: Outline & Research

### Research Tasks

No research needed - all technical decisions are specified:
- Next.js 16 App Router: From constitution and reference-code-uneeza
- Better Auth v1.0.0: Specified in feature description and constitution
- Shadcn UI + Tailwind CSS: From reference-code-uneeza pattern
- JWT shared secret: Matches existing FastAPI backend (already implemented)

---

## Phase 1: Design & Contracts

### Data Model (Frontend Types)

Based on spec requirements and backend API contracts:

```typescript
// types/task.ts
interface Task {
  id: string;              // UUID from backend
  user_id: string;         // Better Auth UUID
  title: string;           // max 200 chars
  description?: string;    // max 1000 chars, optional
  completed: boolean;
  priority: 'High' | 'Medium' | 'Low';
  due_date?: string;       // ISO date string YYYY-MM-DD
  tags: string[];          // Tag names
  created_at: string;      // ISO datetime
  updated_at: string;      // ISO datetime
}

interface TagWithUsage {
  name: string;
  usage_count: number;
}

interface TaskCreate {
  title: string;
  description?: string;
  priority: 'High' | 'Medium' | 'Low';
  due_date?: string;
  tags?: string[];
}

interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'High' | 'Medium' | 'Low';
  due_date?: string;
  tags?: string[];
}

interface TaskFilters {
  completed?: boolean;
  search?: string;
  priority?: 'High' | 'Medium' | 'Low' | 'all';
  tags?: string[];
  sort_by?: 'created_at' | 'updated_at' | 'title' | 'due_date' | 'priority';
  sort_direction?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}
```

### API Contracts

All contracts defined by existing FastAPI backend at `phase-2-todo-full-stack/backend/`:

| Method | Endpoint | Request | Response |
|--------|----------|---------|----------|
| POST | `/api/{user_id}/tasks` | TaskCreate | Task |
| GET | `/api/{user_id}/tasks` | Query params (filters) | Task[] |
| GET | `/api/{user_id}/tasks/{task_id}` | - | Task |
| PUT | `/api/{user_id}/tasks/{task_id}` | TaskUpdate | Task |
| DELETE | `/api/{user_id}/tasks/{task_id}` | - | 204 No Content |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | - | Task |
| GET | `/api/{user_id}/tags` | - | TagWithUsage[] |

### Quick Start Guide

```markdown
# Quick Start: Next.js 16 Todo Frontend

## Prerequisites

- Node.js 18+ (LTS recommended)
- npm, yarn, or pnpm package manager
- FastAPI backend running at http://localhost:8000
- BETTER_AUTH_SECRET from backend .env

## Installation

```bash
cd phase-2-todo-full-stack/frontend
npm install
```

## Environment Setup

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-shared-secret-from-backend
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Development

```bash
npm run dev
```

Visit http://localhost:3000

## Building for Production

```bash
npm run build
npm start
```
```

---

## Phase 2: Tasks Generation

Ready for `/sp.tasks` command to generate implementation tasks based on this plan.

**Artifacts Created**:
- [x] plan.md (this file)
- [x] research.md - No additional research needed (all tech decisions specified)
- [x] data-model.md - Complete TypeScript interface definitions
- [x] quickstart.md - Comprehensive setup and development guide
- [x] contracts/api-contracts.md - All 7 API endpoints documented
- [x] contracts/types.md - API request/response TypeScript types

**Next Command**: `/sp.tasks` to generate implementation tasks.md
