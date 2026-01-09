# Data Model: Next.js 16 Todo Frontend

**Feature**: Next.js 16 Todo Frontend
**Date**: 2025-12-30
**Source**: [plan.md](./plan.md)

## Frontend Type Definitions

These TypeScript interfaces define the types used throughout the frontend application for type safety and API integration.

### Task Types

```typescript
// types/task.ts

/**
 * Task entity from the FastAPI backend
 */
interface Task {
  /** UUID from backend database */
  id: string;
  /** Better Auth UUID of task owner */
  user_id: string;
  /** Task title, max 200 characters */
  title: string;
  /** Task description, max 1000 characters, optional */
  description?: string;
  /** Completion status */
  completed: boolean;
  /** Priority level */
  priority: 'High' | 'Medium' | 'Low';
  /** Due date in ISO format, optional */
  due_date?: string;
  /** Array of tag names */
  tags: string[];
  /** Creation timestamp ISO string */
  created_at: string;
  /** Last update timestamp ISO string */
  updated_at: string;
}

/**
 * Tag with usage count from backend
 */
interface TagWithUsage {
  /** Tag name */
  name: string;
  /** Number of tasks using this tag */
  usage_count: number;
}

/**
 * Task creation payload
 */
interface TaskCreate {
  /** Task title, required, max 200 characters */
  title: string;
  /** Optional description, max 1000 characters */
  description?: string;
  /** Priority level, default: Medium */
  priority: 'High' | 'Medium' | 'Low';
  /** Optional due date in YYYY-MM-DD format */
  due_date?: string;
  /** Optional array of tag names */
  tags?: string[];
}

/**
 * Task update payload (partial update)
 */
interface TaskUpdate {
  /** Optional title update */
  title?: string;
  /** Optional description update */
  description?: string;
  /** Optional completion status update */
  completed?: boolean;
  /** Optional priority update */
  priority?: 'High' | 'Medium' | 'Low';
  /** Optional due date update */
  due_date?: string;
  /** Optional tags update (replaces all) */
  tags?: string[];
}
```

### Filter Types

```typescript
// types/filters.ts

/**
 * Task filter parameters for API queries
 */
interface TaskFilters {
  /** Filter by completion status */
  completed?: boolean;
  /** Search text for title/description matching */
  search?: string;
  /** Filter by priority level */
  priority?: 'High' | 'Medium' | 'Low' | 'all';
  /** Filter by tag names (AND/OR logic per API) */
  tags?: string[];
  /** Sort field */
  sort_by?: 'created_at' | 'updated_at' | 'title' | 'due_date' | 'priority';
  /** Sort direction */
  sort_direction?: 'asc' | 'desc';
  /** Number of results per page, default: 50 */
  limit?: number;
  /** Pagination offset, default: 0 */
  offset?: number;
}

/**
 * Pagination response metadata
 */
interface PaginationMeta {
  /** Total number of tasks matching filters */
  total: number;
  /** Current offset */
  offset: number;
  /** Current limit */
  limit: number;
  /** Whether more results exist */
  has_more: boolean;
}

/**
 * Paginated task response
 */
interface TaskListResponse {
  /** Array of tasks */
  tasks: Task[];
  /** Pagination metadata */
  meta: PaginationMeta;
}
```

### Auth Types

```typescript
// types/auth.ts

/**
 * User session from Better Auth
 */
interface UserSession {
  /** User ID (UUID) */
  id: string;
  /** User email */
  email: string;
  /** Session token */
  token: string;
  /** Session expiration */
  expires_at: Date;
}

/**
 * Sign-up form data
 */
interface SignUpForm {
  /** User email address */
  email: string;
  /** User password (min 8 characters) */
  password: string;
  /** Password confirmation */
  confirmPassword: string;
}

/**
 * Sign-in form data
 */
interface SignInForm {
  /** User email address */
  email: string;
  /** User password */
  password: string;
}
```

## Type Usage Guidelines

1. **API Responses**: Always use `Task` interface when handling responses from the backend
2. **Form Submissions**: Use `TaskCreate` for new tasks, `TaskUpdate` for edits
3. **Filtering**: Construct `TaskFilters` objects from UI state
4. **Pagination**: Destructure `TaskListResponse` for list rendering
5. **Type Safety**: Use strict TypeScript checking (`tsc --strict`)

## Related Files

- `types/task.ts` - Task type definitions
- `types/filters.ts` - Filter and pagination types
- `types/auth.ts` - Authentication types
- `lib/api-client.ts` - API client with type-safe methods
