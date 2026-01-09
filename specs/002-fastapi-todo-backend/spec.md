# Feature Specification: FastAPI Todo Backend (Phase II)

**Feature Branch**: `002-fastapi-todo-backend`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Define the specification for a Production-Ready FastAPI Backend for the Todo App (Phase II).

  **Description**: A secure, multi-tenant API that allows users to manage their personal task lists. The system must act as a stateless backend that validates user identity via tokens and provides strictly isolated data access.

  **Priority**: P1 for Create/View/Toggle/Get Single, P2 for Edit, P3 for Delete

  **Acceptance Criteria**: Valid requests return 201/200, invalid input returns 400, unauthenticated returns 401, accessing other users' data returns 403

  **Key Requirements**:
  - User stories about task management (create, read, update, delete)
  - Security: JWT validation with BETTER_AUTH_SECRET, URL user_id must match JWT sub claim, strict user data isolation
  - Statelessness constraint (no session state between requests)
  - Multi-tenant architecture (strict data isolation per user)
  - RESTful API design with proper HTTP status codes
  - Integration with Better Auth (JWT tokens) and Neon PostgreSQL
  - Input validation, error handling, and CORS configuration
  - Performance: Support 1000 concurrent users, 95% responses under 1 second
  - Database connection pooling for serverless environment"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Task (Priority: P1)

As an authenticated user, I can create new tasks with a title (required, 1-200 characters), optional description (0-1000 characters), optional priority (High/Medium/Low, default: Medium), optional due date, and optional tags so that I can organize and track what I need to do.

**Why this priority**: This is the foundational feature that allows users to begin using the task manager. Without the ability to create tasks, other functionality is meaningless.

**Independent Test**: Can be fully tested by creating a new task with valid input and verifying the system returns a 201 Created response with the task data including a unique ID and timestamps.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a valid JWT token, **When** submitting a task with a valid title (1-200 chars) and optional description, **Then** the task is created and returns 201 Created with task data
2. **Given** an authenticated user, **When** submitting a task with a title exceeding 200 characters, **Then** the system returns 400 Bad Request with a validation error
3. **Given** an authenticated user, **When** submitting a task with an empty title, **Then** the system returns 400 Bad Request with a validation error
4. **Given** an unauthenticated user, **When** submitting a task, **Then** the system returns 401 Unauthorized

---

### User Story 2 - View All Tasks (Priority: P1)

As an authenticated user, I can list all my tasks with optional filtering by status (pending/completed) and pagination so that I can see my current workload.

**Why this priority**: This is essential functionality that allows users to view and manage their tasks. Without this, users cannot effectively use the task manager.

**Independent Test**: Can be fully tested by requesting a list of tasks and verifying only the authenticated user's own tasks are returned, not tasks from other users.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** requesting their tasks without filters, **Then** the system returns an array of the user's tasks with 200 OK
2. **Given** an authenticated user, **When** requesting tasks with status=pending filter, **Then** the system returns only pending tasks with 200 OK
3. **Given** an authenticated user, **When** requesting tasks with pagination (limit and offset), **Then** the system returns paginated results with 200 OK
4. **Given** an authenticated user, **When** the URL contains a user_id that does not match the JWT sub claim, **Then** the system returns 403 Forbidden

---

### User Story 3 - Toggle Task Completion (Priority: P1)

As an authenticated user, I can mark tasks as complete or pending so that I can track my progress on different items.

**Why this priority**: This allows users to update the status of their tasks, which is a core function of a task manager.

**Independent Test**: Can be fully tested by toggling a task's completion status and verifying the status changes correctly.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a pending task, **When** toggling to complete, **Then** the task's completed field changes to true with 200 OK
2. **Given** an authenticated user with a completed task, **When** toggling to pending, **Then** the task's completed field changes to false with 200 OK
3. **Given** an authenticated user, **When** toggling a non-existent task, **Then** the system returns 404 Not Found
4. **Given** an authenticated user, **When** toggling another user's task, **Then** the system returns 403 Forbidden

---

### User Story 4 - Get Single Task (Priority: P1)

As an authenticated user, I can retrieve a specific task by ID so that I can view details of one task.

**Why this priority**: This is needed for viewing task details and enables the editing workflow.

**Independent Test**: Can be fully tested by requesting a specific task and verifying the task data is returned.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** requesting an existing task that belongs to them, **Then** the system returns the task data with 200 OK
2. **Given** an authenticated user, **When** requesting a non-existent task, **Then** the system returns 404 Not Found
3. **Given** an authenticated user, **When** requesting another user's task, **Then** the system returns 403 Forbidden

---

### User Story 5 - Edit Task (Priority: P2)

As an authenticated user, I can update task title and/or description so that I can correct or improve task details.

**Why this priority**: This allows users to maintain accurate task information as requirements change. Important but secondary to core CRUD operations.

**Independent Test**: Can be fully tested by updating a task's details and verifying the changes are reflected in the system.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** updating a task with a valid title, **Then** the task is updated with 200 OK
2. **Given** an authenticated user, **When** updating a task with a title exceeding 200 characters, **Then** the system returns 400 Bad Request
3. **Given** an authenticated user, **When** updating a non-existent task, **Then** the system returns 404 Not Found
4. **Given** an authenticated user, **When** updating another user's task, **Then** the system returns 403 Forbidden

---

### User Story 6 - Delete Task (Priority: P3)

As an authenticated user, I can permanently remove tasks so that I can clean up my task list.

**Why this priority**: This allows users to clean up their task list by removing outdated or unnecessary tasks. Lower priority as users can simply not complete unwanted tasks.

**Independent Test**: Can be fully tested by deleting a task and verifying the system returns 204 No Content.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** deleting their own task, **Then** the system returns 204 No Content
2. **Given** an authenticated user, **When** deleting a non-existent task, **Then** the system returns 404 Not Found
3. **Given** an authenticated user, **When** deleting another user's task, **Then** the system returns 403 Forbidden

---

### User Story 7 - Search and Filter Tasks (Priority: P2)

As an authenticated user, I can search tasks by text (in title/description), filter by status/priority/tags, and sort by various fields so that I can quickly find specific tasks.

**Why this priority**: This significantly improves usability by allowing users to find tasks quickly in large task lists. Important for power users.

**Independent Test**: Can be fully tested by creating multiple tasks and verifying search/filter/sort operations return correct results.

**Acceptance Scenarios**:

1. **Given** an authenticated user with multiple tasks, **When** searching by text query, **Then** the system returns only tasks matching the query in title or description with 200 OK
2. **Given** an authenticated user, **When** filtering by priority=High, **Then** the system returns only High priority tasks with 200 OK
3. **Given** an authenticated user, **When** filtering by tags=["urgent"], **Then** the system returns only tasks tagged with "urgent" with 200 OK
4. **Given** an authenticated user, **When** sorting by due_date ascending, **Then** the system returns tasks ordered by due date (earliest first) with 200 OK

---

### User Story 8 - Manage Tags (Priority: P2)

As an authenticated user, I can view all my unique tags with usage counts so that I can see which tags I use most frequently and maintain consistent tagging.

**Why this priority**: This enables tag-based organization and provides autocomplete suggestions for consistent tagging across tasks.

**Independent Test**: Can be fully tested by creating tasks with various tags and verifying the tag list endpoint returns correct tags with accurate usage counts.

**Acceptance Scenarios**:

1. **Given** an authenticated user with tasks tagged with ["urgent", "work", "urgent"], **When** requesting tags, **Then** the system returns [{"name": "urgent", "usage_count": 2}, {"name": "work", "usage_count": 1}] with 200 OK
2. **Given** an authenticated user with no tasks, **When** requesting tags, **Then** the system returns an empty array with 200 OK
3. **Given** an authenticated user, **When** another user has different tags, **Then** only the authenticated user's tags are returned (data isolation)

---

### Edge Cases

- What happens when a user tries to create a task with duplicate title?
- How does the system handle concurrent requests to update the same task?
- What happens when the database connection fails during an operation?
- How does the system handle JWT token expiration mid-operation?
- What happens when a user has no tasks - does the system return empty array or null?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST validate JWT tokens on every API request using BETTER_AUTH_SECRET
- **FR-002**: System MUST ensure the user_id in the URL path matches the sub claim in the JWT token
- **FR-003**: System MUST return 401 Unauthorized for requests without a valid JWT token
- **FR-004**: System MUST return 403 Forbidden when a user attempts to access another user's data
- **FR-005**: System MUST create tasks with a required title (1-200 characters) and optional description (0-1000 characters)
- **FR-006**: System MUST assign a unique ID to each task upon creation
- **FR-007**: System MUST return tasks only belonging to the authenticated user (strict user data isolation)
- **FR-008**: System MUST support filtering tasks by status (pending/completed)
- **FR-009**: System MUST support pagination with limit and offset parameters
- **FR-010**: System MUST return proper HTTP status codes: 200, 201, 204, 400, 401, 403, 404
- **FR-011**: System MUST validate all input data using Pydantic models with field constraints
- **FR-012**: System MUST handle errors gracefully with structured error responses
- **FR-013**: System MUST configure CORS to allow requests from the Next.js frontend origin
- **FR-014**: System MUST implement connection pooling optimized for Neon serverless PostgreSQL
- **FR-015**: System MUST be stateless with no session state stored between requests
- **FR-016**: System MUST support 1000 concurrent users
- **FR-017**: System MUST return 95% of responses in under 1 second
- **FR-018**: System MUST update the task's updated_at timestamp whenever a task is modified
- **FR-019**: System MUST return appropriate error messages that clearly indicate what went wrong
- **FR-020**: System MUST support task priority levels: High, Medium, Low (default: Medium)
- **FR-021**: System MUST support optional due dates for tasks in ISO 8601 format (YYYY-MM-DD)
- **FR-022**: System MUST support tagging tasks with user-defined tag names (many-to-many relationship)
- **FR-023**: System MUST support full-text search across task titles and descriptions
- **FR-024**: System MUST support filtering tasks by priority level
- **FR-025**: System MUST support filtering tasks by one or more tags
- **FR-026**: System MUST support sorting tasks by: created_at, updated_at, title, due_date, priority
- **FR-027**: System MUST support ascending and descending sort directions
- **FR-028**: System MUST provide tag autocomplete with usage counts for each user

### Key Entities

- **Task**: Represents a user's task with properties: id (UUID), user_id (Better Auth user ID), title (string, 1-200 chars), description (optional string, 0-1000 chars), completed (boolean), priority (enum: High/Medium/Low, default: Medium), due_date (optional ISO 8601 date), created_at (timestamp), updated_at (timestamp), tags (list of tag names via many-to-many relationship)
- **Tag**: Represents a user-defined tag with properties: id (UUID), name (string, unique per user), user_id (Better Auth user ID for data isolation)
- **TaskTag**: Junction table for many-to-many relationship between tasks and tags with properties: task_id (foreign key), tag_id (foreign key)
- **User**: Represented by Better Auth user ID (UUID string) extracted from JWT sub claim
- **TaskCreate**: Schema for creating a new task (title, optional description, optional priority, optional due_date, optional tags list)
- **TaskUpdate**: Schema for updating a task (optional title, optional description, optional completed, optional priority, optional due_date, optional tags list)
- **TaskResponse**: Schema for task API responses (all task fields including tags as list of strings)
- **TagWithUsage**: Schema for tag autocomplete responses (name, usage_count)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, view, edit, delete, and toggle tasks through the API with proper authentication
- **SC-002**: System enforces strict user data isolation - users can only access their own tasks
- **SC-003**: System handles 1000 concurrent users without degradation
- **SC-004**: 95% of API responses complete in under 1 second
- **SC-005**: 100% of authentication tests pass (valid tokens accepted, invalid tokens rejected, wrong user_id rejected)
- **SC-006**: All validation errors return clear, actionable error messages
- **SC-007**: System maintains stateless architecture with no session storage between requests
- **SC-008**: Database connection pooling supports serverless environment with Neon PostgreSQL

## Assumptions

- JWT tokens are issued by Next.js frontend using Better Auth with shared BETTER_AUTH_SECRET
- User IDs are UUID strings from Better Auth
- Task IDs are UUIDs (not auto-incrementing integers)
- Tasks are permanently deleted (no soft delete specified)
- Tags are permanently deleted when no tasks reference them (cascade delete)
- Pagination uses limit/offset pattern (not cursor-based)
- Search uses case-insensitive full-text matching on title and description fields
- Sorting defaults to created_at descending (newest first) when not specified
- No bulk operations specified - only single task operations
- Priority is stored as enum (High/Medium/Low) with Medium as default
- Due dates are optional and stored as ISO 8601 date strings (YYYY-MM-DD)
- Tags are user-specific (different users can have tags with the same name)
- Tag names are case-sensitive and must be unique per user
