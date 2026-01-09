# API Request/Response Types

**Feature**: Next.js 16 Todo Frontend
**Date**: 2025-12-30

## Request Types

### TaskCreateRequest

```typescript
interface TaskCreateRequest {
  title: string;
  description?: string;
  priority: 'High' | 'Medium' | 'Low';
  due_date?: string;
  tags?: string[];
}
```

### TaskUpdateRequest

```typescript
interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'High' | 'Medium' | 'Low';
  due_date?: string;
  tags?: string[];
}
```

### TaskListRequest

```typescript
interface TaskListRequest {
  search?: string;
  completed?: boolean;
  priority?: 'High' | 'Medium' | 'Low' | 'all';
  tags?: string;
  sort_by?: 'created_at' | 'updated_at' | 'title' | 'due_date' | 'priority';
  sort_direction?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}
```

### SignUpRequest

```typescript
interface SignUpRequest {
  email: string;
  password: string;
}
```

### SignInRequest

```typescript
interface SignInRequest {
  email: string;
  password: string;
}
```

## Response Types

### TaskResponse

```typescript
interface TaskResponse {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'High' | 'Medium' | 'Low';
  due_date?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}
```

### TaskListResponse

```typescript
interface TaskListResponse {
  tasks: TaskResponse[];
  meta: {
    total: number;
    limit: number;
    offset: number;
    has_more: boolean;
  };
}
```

### TagWithUsageResponse

```typescript
interface TagWithUsageResponse {
  name: string;
  usage_count: number;
}
```

### SignInResponse

```typescript
interface SignInResponse {
  token: string;
  user: {
    id: string;
    email: string;
  };
}
```

### ErrorResponse

```typescript
interface ErrorResponse {
  detail: string;
}
```
