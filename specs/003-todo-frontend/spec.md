# Feature Specification: Next.js 16 Todo Frontend

**Feature Branch**: `003-todo-frontend`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Create Next.js 16 frontend for Phase 2 Todo application with Better Auth integration, connecting to completed FastAPI backend at phase-2-todo-full-stack/backend/ with JWT shared secret authentication, task CRUD operations (create, read, update, delete, toggle completion), search/filter/sort/pagination, tags with usage counts, using reference-code-uneeza pattern with Shadcn UI and Tailwind CSS"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication (Priority: P1)

As a user, I want to sign up and sign in to the Todo application so that I can securely access my tasks.

**Why this priority**: Authentication is the foundation - without it, no other feature can work. MVP must have working auth.

**Independent Test**: A new user can complete sign-up flow, receive confirmation, and access the dashboard with their tasks from the backend.

**Acceptance Scenarios**:

1. **Given** the user is on the home page, **When** they click "Sign Up", **Then** they should see a sign-up form with email and password fields
2. **Given** the user enters valid credentials, **When** they submit the form, **Then** they should be redirected to the dashboard
3. **Given** an authenticated user, **When** they visit the home page, **Then** they should be redirected to the dashboard
4. **Given** an authenticated user, **When** they click "Sign Out", **Then** they should be redirected to the home page and their session should be cleared

---

### User Story 2 - View Task List (Priority: P1)

As an authenticated user, I want to see all my tasks in a list so that I can track what I need to do.

**Why this priority**: Core functionality - users need to see their tasks to manage them. Connected to the completed GET `/api/{user_id}/tasks` endpoint.

**Independent Test**: User sees their tasks rendered from the FastAPI backend with proper loading states and error handling.

**Acceptance Scenarios**:

1. **Given** an authenticated user with tasks, **When** they visit the dashboard, **Then** they should see a list of all their tasks with title, completion status, priority, and tags
2. **Given** an authenticated user with no tasks, **When** they visit the dashboard, **Then** they should see an empty state with a "Create your first task" prompt
3. **Given** an authenticated user, **When** their tasks are loading, **Then** they should see a loading skeleton or spinner
4. **Given** an authenticated user, **When** the API fails, **Then** they should see an error message with retry option

---

### User Story 3 - Create Task (Priority: P1)

As an authenticated user, I want to create a new task with title, description, priority, due date, and tags so that I can add items to my todo list.

**Why this priority**: Core functionality - users need to add tasks. Connected to the completed POST `/api/{user_id}/tasks` endpoint with all advanced fields.

**Independent Test**: User can fill out a task form with all fields and see the new task appear in their list.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they click "Add Task", **Then** they should see a form with title (required), description (optional), priority (High/Medium/Low), due date (optional), and tags (comma-separated)
2. **Given** a user fills in a valid title, **When** they submit the form, **Then** the task should be created via the API and appear in the list
3. **Given** a user submits without a title, **Then** they should see a validation error
4. **Given** a user adds tags separated by commas, **When** the task is created, **Then** the tags should be stored and displayed on the task

---

### User Story 4 - Toggle Task Completion (Priority: P2)

As an authenticated user, I want to mark tasks as complete or incomplete so that I can track my progress.

**Why this priority**: Essential workflow - users need to mark tasks as done. Connected to PATCH `/api/{user_id}/tasks/{task_id}/complete`.

**Independent Test**: User can click a checkbox to toggle task completion and see the visual state change immediately.

**Acceptance Scenarios**:

1. **Given** a pending task, **When** the user clicks the checkbox, **Then** the task should be marked as complete and the UI should update
2. **Given** a completed task, **When** the user clicks the checkbox, **Then** the task should be marked as pending
3. **Given** a user toggles a task, **When** the API call succeeds, **Then** the change should persist
4. **Given** a user toggles a task, **When** the API call fails, **Then** the UI should revert and show an error

---

### User Story 5 - Edit Task (Priority: P2)

As an authenticated user, I want to edit task details so that I can update or correct my tasks.

**Why this priority**: Common workflow - users need to modify tasks. Connected to PUT `/api/{user_id}/tasks/{task_id}`.

**Independent Test**: User can open a task in edit mode, modify any field, and save changes.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the user clicks "Edit", **Then** they should see a pre-filled form with current values
2. **Given** a user modifies task fields, **When** they click "Save", **Then** the changes should be sent to the API
3. **Given** a user modifies the title to be empty, **When** they click "Save", **Then** they should see a validation error
4. **Given** a user modifies tags, **When** they save, **Then** the old tags should be replaced with new ones

---

### User Story 6 - Delete Task (Priority: P3)

As an authenticated user, I want to delete tasks so that I can remove items I no longer need.

**Why this priority**: Standard feature - cleanup functionality. Connected to DELETE `/api/{user_id}/tasks/{task_id}`.

**Independent Test**: User can delete a task with confirmation, and the task disappears from the list.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the user clicks "Delete", **Then** they should see a confirmation dialog
2. **Given** the user confirms deletion, **When** the API succeeds, **Then** the task should be removed from the list
3. **Given** the user cancels deletion, **Then** the task should remain unchanged

---

### User Story 7 - Search and Filter Tasks (Priority: P2)

As an authenticated user with many tasks, I want to search and filter so that I can quickly find specific tasks.

**Why this priority**: Usability for power users with many tasks. Connected to GET `/api/{user_id}/tasks` with search, priority, tags, sort, limit, offset query params.

**Independent Test**: User can search text, filter by priority/tags, sort by different fields, and see paginated results.

**Acceptance Scenarios**:

1. **Given** tasks exist, **When** the user types in search, **Then** the list should filter to matching tasks (title/description)
2. **Given** tasks exist, **When** the user selects "High" priority filter, **Then** only High priority tasks should appear
3. **Given** tasks have tags, **When** the user selects tags, **Then** tasks with ANY selected tag should appear
4. **Given** multiple tasks exist, **When** the user sorts by "due_date" ascending, **Then** tasks should be ordered by due date
5. **Given** many tasks exist, **When** the user scrolls to the bottom, **Then** pagination should load more tasks

---

### User Story 8 - View Tags (Priority: P2)

As an authenticated user, I want to see all my tags with usage counts so that I can organize and filter my tasks effectively.

**Why this priority**: Tag management for organization. Connected to GET `/api/{user_id}/tags` with TagWithUsage response.

**Independent Test**: User can see a list of all their tags sorted alphabetically with task counts.

**Acceptance Scenarios**:

1. **Given** a user has created tasks with tags, **When** they view the tags section, **Then** they should see all unique tags sorted alphabetically
2. **Given** a tag is used on multiple tasks, **When** viewed, **Then** the usage count should show the number of tasks
3. **Given** a user has no tags, **When** they view the tags section, **Then** they should see an empty state

---

### Edge Cases

- What happens when the backend is unavailable (network error)?
- How does the system handle expired JWT tokens?
- What happens when two tabs are open and changes are made in one?
- How does the system handle very long task titles (>200 chars)?
- What happens when tags are duplicated during creation?
- How does the UI handle mobile vs desktop screen sizes?
- What happens during concurrent task updates (race conditions)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to sign up with email and password using Better Auth
- **FR-002**: System MUST allow users to sign in with email and password using Better Auth
- **FR-003**: System MUST allow users to sign out and clear their session
- **FR-004**: System MUST display all tasks belonging to the authenticated user via GET `/api/{user_id}/tasks`
- **FR-005**: System MUST allow users to create tasks with title, description, priority, due_date, and tags via POST `/api/{user_id}/tasks`
- **FR-006**: System MUST allow users to toggle task completion status via PATCH `/api/{user_id}/tasks/{task_id}/complete`
- **FR-007**: System MUST allow users to edit task details via PUT `/api/{user_id}/tasks/{task_id}`
- **FR-008**: System MUST allow users to delete tasks with confirmation via DELETE `/api/{user_id}/tasks/{task_id}`
- **FR-009**: System MUST allow users to search tasks by title/description via `search` query param
- **FR-010**: System MUST allow users to filter tasks by priority via `priority` query param
- **FR-011**: System MUST allow users to filter tasks by tags via `tags` query param
- **FR-012**: System MUST allow users to sort tasks by created_at, due_date, priority, title via `sort_by` and `sort_direction` params
- **FR-013**: System MUST paginate task results with `limit` and `offset` params (default 50, max 100)
- **FR-014**: System MUST display all user tags with usage counts via GET `/api/{user_id}/tags`
- **FR-015**: System MUST validate JWT token with shared BETTER_AUTH_SECRET against FastAPI backend
- **FR-016**: System MUST enforce user_id matching between URL path and JWT sub claim
- **FR-017**: System MUST handle 401 responses by redirecting to sign-in page
- **FR-018**: System MUST handle 403 responses by showing authorization error
- **FR-019**: System MUST show loading states during API calls
- **FR-020**: System MUST show error messages with retry options on API failure
- **FR-021**: System MUST persist session across browser refreshes via httpOnly cookies
- **FR-022**: System MUST use Shadcn UI components for consistent design
- **FR-023**: System MUST use Tailwind CSS for styling
- **FR-024**: System MUST follow reference-code-uneeza project structure and patterns

### Key Entities

- **User**: Authenticated user with session from Better Auth
- **Task**: User-created todo item with:
  - id (UUID)
  - user_id (Better Auth UUID)
  - title (max 200 chars)
  - description (max 1000 chars, optional)
  - completed (boolean)
  - priority (High/Medium/Low, default: Medium)
  - due_date (optional date)
  - tags (many-to-many via junction table)
  - created_at, updated_at timestamps
- **Tag**: User-scoped tag with:
  - id (UUID)
  - user_id (Better Auth UUID)
  - name (max 50 chars)
  - usage_count (computed from task associations)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete authentication flow in under 30 seconds
- **SC-002**: Task list loads within 2 seconds for up to 100 tasks
- **SC-003**: Task CRUD operations complete with visual feedback within 1 second
- **SC-004**: Search and filter results appear within 500ms of input
- **SC-005**: Zero unauthorized access - all endpoints properly validate JWT and user_id
- **SC-006**: Responsive design works on mobile (320px+) and desktop (1200px+)
- **SC-007**: All 7 FastAPI API endpoints are integrated and tested
- **SC-008**: All JWT auth flows work with the FastAPI backend using shared secret
- **SC-009**: 100% of user-facing flows have loading and error states
