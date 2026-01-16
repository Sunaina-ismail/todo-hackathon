# API Contract: ChatKit Endpoint

**Feature**: 004-ai-chatbot
**Date**: 2026-01-12
**Phase**: Phase 1 - API Contracts

## Overview

This document defines the API contract for the `/api/chatkit` endpoint, which implements the official ChatKit protocol for conversational AI task management. The endpoint handles all ChatKit protocol requests including thread management, message streaming, and widget rendering.

---

## Endpoint Specification

### POST /api/chatkit

**Description**: ChatKit protocol endpoint for AI-powered task management

**Protocol**: Official ChatKit Protocol (https://github.com/openai/chatkit-js)

**Authentication**: Required - JWT Bearer token

**Content-Type**: `application/json`

**Response Types**:
- `text/event-stream` (SSE) - For streaming responses
- `application/json` - For non-streaming responses

---

## Authentication

### JWT Bearer Token

**Header**:
```
Authorization: Bearer <jwt_token>
```

**JWT Payload**:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234567890
}
```

**Validation**:
- JWT signature verified using `BETTER_AUTH_SECRET`
- `user_id` extracted from `sub` claim
- `user_id` passed to ChatKit server in request context
- All MCP tools validate `user_id` matches authenticated user

**Error Responses**:
- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - JWT valid but user not authorized

---

## Request Format

### ChatKit Protocol Request

The request body follows the official ChatKit protocol specification.

**Common Request Types**:

1. **Create Thread**
2. **Send Message**
3. **Get Thread**
4. **List Threads**
5. **Widget Rendering**

**Example Request (Send Message)**:
```json
{
  "type": "thread.message.create",
  "thread_id": "thread_abc123",
  "message": {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "Add a task to buy groceries"
      }
    ]
  }
}
```

**Request Fields**:
- `type` (string, required): ChatKit protocol message type
- `thread_id` (string, optional): Thread identifier (null for new threads)
- `message` (object, optional): Message content for message creation
- Additional fields per ChatKit protocol specification

---

## Response Format

### Streaming Response (SSE)

**Content-Type**: `text/event-stream`

**Event Format**:
```
event: thread.item.added
data: {"type":"thread.item.added","item":{"id":"msg_123","type":"assistant_message","content":[{"type":"text","text":"I've added..."}]}}

event: thread.item.updated
data: {"type":"thread.item.updated","item":{"id":"msg_123","type":"assistant_message","content":[{"type":"text","text":"I've added 'Buy groceries'..."}]}}

event: thread.item.completed
data: {"type":"thread.item.completed","item":{"id":"msg_123"}}
```

**Event Types**:
- `thread.item.added` - New item added to thread (message, tool call, etc.)
- `thread.item.updated` - Existing item updated (streaming text)
- `thread.item.completed` - Item processing completed
- `thread.updated` - Thread metadata updated (title, etc.)
- `progress.update` - Progress indicator update

**Event Data**:
- `type` (string): Event type
- `item` (object): Event payload (varies by type)
- Additional fields per ChatKit protocol

### JSON Response

**Content-Type**: `application/json`

**Success Response**:
```json
{
  "thread": {
    "id": "thread_abc123",
    "title": "New Conversation",
    "created_at": "2026-01-12T10:30:00Z",
    "updated_at": "2026-01-12T10:30:00Z"
  },
  "messages": [
    {
      "id": "msg_123",
      "role": "user",
      "content": [{"type": "text", "text": "Add a task to buy groceries"}],
      "created_at": "2026-01-12T10:30:00Z"
    },
    {
      "id": "msg_456",
      "role": "assistant",
      "content": [{"type": "text", "text": "I've added 'Buy groceries' to your tasks."}],
      "created_at": "2026-01-12T10:30:05Z"
    }
  ]
}
```

**Error Response**:
```json
{
  "error": "Internal server error",
  "message": "Failed to process request",
  "code": "CHATKIT_ERROR"
}
```

---

## MCP Tools Integration

The ChatKit endpoint integrates with 7 MCP tools for task operations:

### Tool: add_task

**Purpose**: Create a new task for a user

**Parameters**:
- `user_id` (string, required): User's unique identifier from JWT
- `title` (string, required): Task title (max 200 characters)
- `description` (string, optional): Task description (max 1000 characters)
- `priority` (string, optional): "low" | "medium" | "high" (auto-detected if not provided)
- `due_date` (string, optional): ISO 8601 date or natural language ("tomorrow", "next friday")

**Returns**:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "created",
  "title": "Buy groceries",
  "priority": "medium",
  "due_date": "2026-01-13"
}
```

### Tool: list_tasks

**Purpose**: Retrieve tasks with optional filtering

**Parameters**:
- `user_id` (string, required): User's unique identifier from JWT
- `status` (string, optional): "all" | "pending" | "completed" (default: "all")
- `priority` (string, optional): "low" | "medium" | "high"
- `search` (string, optional): Search keyword for title/description

**Returns**:
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": null,
      "completed": false,
      "priority": "medium",
      "due_date": "2026-01-13",
      "created_at": "2026-01-12T10:30:00Z",
      "updated_at": "2026-01-12T10:30:00Z"
    }
  ],
  "count": 1,
  "total": 1
}
```

### Tool: complete_task

**Purpose**: Mark a task as complete

**Parameters**:
- `user_id` (string, required): User's unique identifier from JWT
- `task_id` (string, required): Task UUID to mark as complete

**Returns**:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "title": "Buy groceries"
}
```

### Tool: delete_task

**Purpose**: Remove a task from the todo list

**Parameters**:
- `user_id` (string, required): User's unique identifier from JWT
- `task_id` (string, required): Task UUID to delete

**Returns**:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "deleted",
  "title": "Buy groceries"
}
```

### Tool: update_task

**Purpose**: Modify task details

**Parameters**:
- `user_id` (string, required): User's unique identifier from JWT
- `task_id` (string, required): Task UUID to update
- `title` (string, optional): New task title
- `description` (string, optional): New task description
- `priority` (string, optional): New priority level
- `completed` (boolean, optional): New completion status
- `tags` (array, optional): New list of tags

**Returns**:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "updated",
  "title": "Buy groceries and fruits",
  "priority": "high",
  "completed": false,
  "tags": ["shopping"]
}
```

### Tool: set_priority

**Purpose**: Update task priority level

**Parameters**:
- `user_id` (string, required): User's unique identifier from JWT
- `task_id` (string, required): Task UUID to update
- `priority` (string, required): "low" | "medium" | "high"

**Returns**:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "updated",
  "priority": "high",
  "title": "Buy groceries"
}
```

### Tool: get_task

**Purpose**: Retrieve a single task by ID

**Parameters**:
- `user_id` (string, required): User's unique identifier from JWT
- `task_id` (string, required): Task UUID to retrieve

**Returns**:
```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": null,
    "completed": false,
    "priority": "medium",
    "due_date": "2026-01-13",
    "created_at": "2026-01-12T10:30:00Z",
    "updated_at": "2026-01-12T10:30:00Z"
  },
  "message": "Task retrieved successfully"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": "Error type",
  "message": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes

| Status Code | Description | Example |
|-------------|-------------|---------|
| 200 OK | Successful request | Thread created, message sent |
| 401 Unauthorized | Missing or invalid JWT | No Authorization header |
| 403 Forbidden | User not authorized | JWT valid but user lacks permission |
| 404 Not Found | Resource not found | Thread or task doesn't exist |
| 422 Unprocessable Entity | Invalid request data | Malformed JSON, missing required fields |
| 500 Internal Server Error | Server error | Database connection failed, agent error |

### Common Error Scenarios

**Authentication Errors**:
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid JWT token",
  "code": "AUTH_REQUIRED"
}
```

**User Isolation Violation**:
```json
{
  "error": "Forbidden",
  "message": "Task not found or you don't have permission to access it",
  "code": "ACCESS_DENIED"
}
```

**Invalid Task Reference**:
```json
{
  "error": "Not Found",
  "message": "Task not found or you don't have permission to access it",
  "code": "TASK_NOT_FOUND"
}
```

**Agent Processing Error**:
```json
{
  "error": "Internal Server Error",
  "message": "Failed to process request",
  "code": "AGENT_ERROR"
}
```

---

## Performance Characteristics

### Response Times

- **Initial Response**: < 1 second (streaming starts immediately)
- **Tool Execution**: 100-500ms per tool call
- **LLM Response**: 1-3 seconds for complete response
- **Total Request**: 2-5 seconds for typical conversation turn

### Concurrency

- **Concurrent Users**: Supports 100+ simultaneous conversations
- **Connection Pooling**: Database connections reused via async session factory
- **Streaming**: SSE connections maintained for duration of response

### Rate Limiting

- **Not Implemented**: No rate limiting in Phase III
- **Future Consideration**: Implement per-user rate limits in Phase IV

---

## Security Considerations

### User Isolation

1. **JWT Validation**: Every request validates JWT signature
2. **User ID Extraction**: `user_id` extracted from JWT `sub` claim
3. **Context Passing**: `user_id` passed to ChatKit server in request context
4. **Tool Validation**: Every MCP tool validates `user_id` matches authenticated user
5. **Database Filtering**: All queries filter by `user_id`

### Data Privacy

1. **Encryption**: All connections use TLS/SSL
2. **Retention**: Messages auto-deleted after 2 days
3. **Logging**: No sensitive data logged (passwords, tokens)
4. **CORS**: Only configured frontend origins allowed

### Input Validation

1. **JSON Schema**: Request body validated against ChatKit protocol schema
2. **Content Length**: Maximum 10,000 characters per message
3. **Sanitization**: HTML stripped from user input
4. **SQL Injection**: Prevented via SQLModel parameterized queries

---

## Testing

### Unit Tests

- Test JWT validation and user_id extraction
- Test request parsing and validation
- Test error handling and response formatting

### Integration Tests

- Test full request/response cycle with real database
- Test streaming responses and SSE format
- Test MCP tool integration and user isolation
- Test concurrent requests and connection pooling

### Example Test Cases

**Test: Successful Message Send**:
```python
async def test_send_message_success():
    response = await client.post(
        "/api/chatkit",
        json={"type": "thread.message.create", "thread_id": "thread_123", "message": {...}},
        headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"
```

**Test: User Isolation**:
```python
async def test_user_isolation():
    # User A creates task
    response_a = await client.post("/api/chatkit", json={...}, headers={"Authorization": f"Bearer {jwt_token_a}"})

    # User B tries to access User A's task
    response_b = await client.post("/api/chatkit", json={"type": "thread.message.create", "message": {"content": "Show task 1"}}, headers={"Authorization": f"Bearer {jwt_token_b}"})

    # User B should not see User A's task
    assert "Task not found" in response_b.text
```

---

## Summary

The `/api/chatkit` endpoint provides:
- ✅ Official ChatKit protocol compliance
- ✅ JWT authentication with user isolation
- ✅ Streaming SSE responses for progressive rendering
- ✅ 7 MCP tools for task operations
- ✅ Comprehensive error handling
- ✅ Performance optimized for 100+ concurrent users
- ✅ Security hardened with input validation and data privacy

All API design aligns with Phase III constitutional requirements for stateless architecture, user isolation, and ChatKit protocol compliance.
