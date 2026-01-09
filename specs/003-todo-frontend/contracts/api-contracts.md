# API Contracts: Next.js 16 Todo Frontend

**Feature**: Next.js 16 Todo Frontend
**Date**: 2025-12-30
**Source**: FastAPI backend at `phase-2-todo-full-stack/backend/`

## Base Configuration

| Property | Value |
|----------|-------|
| Base URL | `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`) |
| Auth Header | `Authorization: Bearer <jwt_token>` |
| Content-Type | `application/json` |

---

## Authentication Endpoints

### POST /api/auth/sign-up

Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2025-12-30T10:00:00Z"
}
```

**Errors:**
- 400: Validation error (email/password too short)
- 409: Email already registered

---

### POST /api/auth/sign-in

Authenticate and receive JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}
```

**Errors:**
- 401: Invalid credentials

---

## Task Endpoints

### POST /api/{user_id}/tasks

Create a new task.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "Medium",
  "due_date": "2025-12-31",
  "tags": ["shopping", "home"]
}
```

**Response (201 Created):**
```json
{
  "id": "task-uuid",
  "user_id": "user-uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "Medium",
  "due_date": "2025-12-31",
  "tags": ["shopping", "home"],
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Errors:**
- 400: Validation error (title too long, invalid priority)
- 401: Unauthorized
- 403: user_id mismatch with JWT

---

### GET /api/{user_id}/tasks

List tasks with optional filtering, sorting, and pagination.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search` | string | - | Text to match in title/description |
| `completed` | boolean | - | Filter by completion status |
| `priority` | string | - | Filter by priority (High/Medium/Low) |
| `tags` | string | - | Comma-separated tag list |
| `sort_by` | string | created_at | Sort field |
| `sort_direction` | string | desc | asc or desc |
| `limit` | number | 50 | Results per page (max 100) |
| `offset` | number | 0 | Pagination offset |

**Example Request:**
```
GET /api/user-uuid/tasks?search=groceries&priority=Medium&sort_by=created_at&sort_direction=desc&limit=20&offset=0
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "task-uuid",
      "user_id": "user-uuid",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "priority": "Medium",
      "due_date": "2025-12-31",
      "tags": ["shopping", "home"],
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z"
    }
  ],
  "meta": {
    "total": 1,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Errors:**
- 401: Unauthorized
- 403: user_id mismatch with JWT

---

### GET /api/{user_id}/tasks/{task_id}

Get a single task by ID.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "task-uuid",
  "user_id": "user-uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "Medium",
  "due_date": "2025-12-31",
  "tags": ["shopping", "home"],
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Errors:**
- 401: Unauthorized
- 403: user_id mismatch with JWT
- 404: Task not found

---

### PUT /api/{user_id}/tasks/{task_id}

Update task details (full update).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request:**
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, vegetables",
  "priority": "High",
  "due_date": "2025-12-31",
  "tags": ["shopping", "cooking", "home"]
}
```

**Response (200 OK):**
```json
{
  "id": "task-uuid",
  "user_id": "user-uuid",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, vegetables",
  "completed": false,
  "priority": "High",
  "due_date": "2025-12-31",
  "tags": ["shopping", "cooking", "home"],
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T11:00:00Z"
}
```

**Errors:**
- 400: Validation error
- 401: Unauthorized
- 403: user_id mismatch with JWT
- 404: Task not found

---

### DELETE /api/{user_id}/tasks/{task_id}

Delete a task.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (204 No Content):** Empty body

**Errors:**
- 401: Unauthorized
- 403: user_id mismatch with JWT
- 404: Task not found

---

### PATCH /api/{user_id}/tasks/{task_id}/complete

Toggle task completion status.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "task-uuid",
  "user_id": "user-uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "priority": "Medium",
  "due_date": "2025-12-31",
  "tags": ["shopping", "home"],
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Errors:**
- 401: Unauthorized
- 403: user_id mismatch with JWT
- 404: Task not found

---

## Tag Endpoints

### GET /api/{user_id}/tags

Get all tags with usage counts for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
[
  {
    "name": "shopping",
    "usage_count": 5
  },
  {
    "name": "home",
    "usage_count": 3
  },
  {
    "name": "work",
    "usage_count": 8
  }
]
```

**Notes:**
- Tags are sorted alphabetically by name
- `usage_count` reflects the number of tasks using each tag

**Errors:**
- 401: Unauthorized
- 403: user_id mismatch with JWT

---

## Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing the issue"
}
```

**Common HTTP Status Codes:**

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Invalid input, validation failed |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | user_id in URL doesn't match JWT sub |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error (detailed) |
| 500 | Internal Server Error | Backend error |

---

## JWT Token Format

Tokens are signed using HS256 algorithm with `BETTER_AUTH_SECRET`.

**Token Payload:**
```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "exp": 1703931600,
  "iat": 1703931000
}
```

- `sub`: User ID (UUID)
- `email`: User email
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

---

## Related Files

- [plan.md](../plan.md) - Implementation plan
- [data-model.md](../data-model.md) - Frontend type definitions
- Backend API: `phase-2-todo-full-stack/backend/app/routers/tasks.py`
