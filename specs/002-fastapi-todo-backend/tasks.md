# Tasks: FastAPI Todo Backend (Phase II)

**Input**: Design documents from `/specs/002-fastapi-todo-backend/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/openapi.yaml
**Feature Branch**: `002-fastapi-todo-backend`
**Project Location**: `phase-2-todo-full-stack/backend/`

## Summary

Production-Ready FastAPI Backend with JWT authentication, Neon PostgreSQL, and advanced features (priority, due_date, tags, search, filtering, sorting). Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US7, US8)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and basic structure for `phase-2-todo-full-stack/backend/`

- [X] T001 Create backend directory structure per plan.md at `phase-2-todo-full-stack/backend/src/`
- [X] T002 [P] Create `pyproject.toml` with FastAPI, SQLModel, Pydantic, python-jose, alembic, pytest dependencies
- [X] T003 [P] Initialize `uv.lock` and virtual environment with `uv sync`
- [X] T004 Create `.env.example` with DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS variables
- [X] T005 [P] Create `Dockerfile` for backend service with Python 3.13
- [X] T006 Create `README.md` with setup and run instructions from quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites) + Advanced Features

**Purpose**: Core infrastructure with advanced features (priority, due_date, tags) that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Core Infrastructure (Original Foundation)

- [X] T007 Create `src/__init__.py` and `src/config.py` with pydantic-settings for environment configuration
- [X] T008 [P] Create `src/db/__init__.py`, `src/db/engine.py` with SQLModel engine and Neon connection pooling (pool_size=5, max_overflow=10, pool_pre_ping=True)
- [X] T009 [P] Create `src/db/session.py` with database session dependency for FastAPI Depends()
- [X] T010 [P] Create `src/models/__init__.py` and `src/models/base.py` with SQLModel declarative base
- [X] T012 [P] Create `src/schemas/__init__.py`, `src/schemas/common.py` for error responses
- [X] T014 Create `src/auth/__init__.py`, `src/auth/jwt.py` with JWT verification using python-jose and BETTER_AUTH_SECRET
- [X] T015 Create `src/auth/dependencies.py` with get_current_user FastAPI dependency and user_id validation
- [X] T016 [P] Create `src/services/__init__.py` and `src/services/exceptions.py` with custom HTTP exceptions
- [X] T017 Create `src/main.py` with FastAPI app, CORS middleware, health endpoint, and global exception handlers
- [X] T020 Create Alembic migration: `alembic/env.py`, `alembic/script.py.mako`, `alembic.ini`
- [X] T021 [P] Create `tests/__init__.py`, `tests/conftest.py` with pytest fixtures and test JWT helper

### Advanced Features - Models (Extends Foundation)

- [X] T011 [P] **UPDATE** `src/models/task.py` with Task entity:
  - Change `id` from Integer to **UUID** (uuid.uuid4)
  - Add `priority` field (PriorityType enum: High/Medium/Low, default: Medium)
  - Add `due_date` field (date, optional)
  - Keep existing: user_id, title, description, completed, created_at, updated_at
  - Add composite index on (user_id, completed)

- [X] T022 [P] Create `src/models/tag.py` with Tag entity:
  - UUID id (uuid.uuid4)
  - name (string, max 50 chars)
  - user_id (string, Better Auth UUID)
  - Unique composite index on (user_id, name)

- [X] T023 [P] Create `src/models/task_tag.py` with TaskTag junction table:
  - task_id (UUID, foreign key to tasks.id, CASCADE delete)
  - tag_id (UUID, foreign key to tags.id, CASCADE delete)
  - Composite primary key (task_id, tag_id)

### Advanced Features - Schemas (Extends Foundation)

- [X] T013 [P] **UPDATE** `src/schemas/task.py` with:
  - PriorityType enum definition (High/Medium/Low)
  - TaskCreate: title, description, **priority** (default: Medium), **due_date** (optional), **tags** (List[str], default: [])
  - TaskUpdate: title, description, completed, **priority**, **due_date**, **tags** (all optional)
  - TaskResponse: all Task fields including **priority**, **due_date**, **tags** (List[str])

- [X] T024 [P] Create `src/schemas/tag.py` with TagWithUsage schema:
  - name (string)
  - usage_count (integer)

### Advanced Features - Services (Extends Foundation)

- [X] T025 [P] Create `src/services/tag_service.py` with methods:
  - get_or_create_tag(session, user_id, tag_name) → Tag
  - get_user_tags_with_usage(session, user_id) → List[TagWithUsage]
  - assign_tags_to_task(session, task, tag_names: List[str])
  - remove_orphaned_tags(session, user_id)

- [X] T018 **UPDATE** `src/services/task_service.py` with:
  - Original methods: create_task, get_tasks, get_task, update_task, delete_task, toggle_completion
  - **NEW** parameters for get_tasks():
    - search_text (case-insensitive ILIKE on title/description)
    - priority_filter (all/High/Medium/Low)
    - tags_filter (List[str])
    - sort_by (created_at/updated_at/title/due_date/priority)
    - sort_direction (asc/desc)
  - **UPDATE** create_task() and update_task() to handle tag assignment

### Advanced Features - API Endpoints (Extends Foundation)

- [X] T019 [P] **UPDATE** `src/api/v1/tasks.py` with all CRUD endpoints:
  - POST /api/{user_id}/tasks (with priority, due_date, tags)
  - GET /api/{user_id}/tasks (with search, priority, tags, sort_by, sort_direction query params)
  - GET /api/{user_id}/tasks/{task_id}
  - PUT/PATCH /api/{user_id}/tasks/{task_id} (with priority, due_date, tags)
  - DELETE /api/{user_id}/tasks/{task_id}
  - PATCH /api/{user_id}/tasks/{task_id}/complete

- [X] T026 [P] Create `src/api/v1/tags.py` with GET `/api/{user_id}/tags` endpoint:
  - Returns TagWithUsage array
  - Uses TagService.get_user_tags_with_usage()
  - Enforces user_id validation (URL vs JWT)

- [X] T027 Register tags router in `src/main.py`:
  - Import tags router from `src/api/v1/tags.py`
  - Add to app with `/api` prefix

### Advanced Features - Database Migrations

- [X] T028 Create Alembic migration `001_update_tasks_add_advanced_fields.py`:
  - Alter tasks.id from INTEGER to UUID (⚠️ requires data migration, destructive)
  - Add priority column (VARCHAR, default 'Medium')
  - Add due_date column (DATE, nullable)
  - Add composite index on (user_id, completed)
  - **CRITICAL**: Backup data before migration

- [X] T029 [P] Create Alembic migration `002_create_tags_table.py`:
  - Create tags table with UUID id, name, user_id
  - Add unique composite index on (user_id, name)

- [X] T030 [P] Create Alembic migration `003_create_task_tags_junction.py`:
  - Create task_tags junction table
  - Add composite primary key (task_id, tag_id)
  - Add foreign keys with CASCADE delete

**Checkpoint**: Foundation with advanced features ready - all user stories can now be implemented

---

## Phase 3: User Story 1 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create new tasks with title, description, **priority**, **due_date**, and **tags**

**Independent Test**: POST to `/api/{user_id}/tasks` with valid JWT returns 201 Created with task data including new fields

### Tests for User Story 1

- [X] T031 [P] [US1] Create `tests/unit/test_models.py` to verify:
  - Task model validation with UUID, priority, due_date
  - Tag model validation
  - TaskTag junction table

- [X] T032 [P] [US1] Create `tests/unit/test_jwt_validation.py` to verify JWT authentication

- [X] T033 [P] [US1] Create `tests/integration/test_task_create.py` with tests for:
  - Valid task creation with priority/due_date/tags returns 201
  - Missing title returns 400
  - Title > 200 chars returns 400
  - Empty title returns 400
  - Invalid priority value returns 400
  - Invalid due_date format returns 400
  - Unauthenticated request returns 401
  - Tags are properly associated with created task

### Implementation for User Story 1

- [X] T034 [US1] Implement POST `/api/{user_id}/tasks` endpoint (already created in T019, ensure it handles new fields)
- [X] T035 [US1] Add user_id validation in endpoint (URL user_id must match JWT sub claim)
- [X] T036 [US1] Integrate TaskService.create_task() with tag assignment
- [X] T037 [US1] Add validation error responses (400) with clear messages per FR-019
- [X] T038 [US1] Add authentication error responses (401, 403)

**Checkpoint**: User Story 1 complete - can create tasks with priority, due_date, and tags

---

## Phase 4: User Story 2 + User Story 7 - View, Search, Filter, Sort Tasks (Priority: P1 + P2)

**Goal**: Authenticated users can list tasks with **search**, **filtering** (status/priority/tags), **sorting** (5 fields), and pagination

**Independent Test**: GET to `/api/{user_id}/tasks?search=groceries&priority=High&tags=urgent&sort_by=due_date&sort_direction=asc` returns filtered and sorted tasks

### Tests for User Story 2 + 7

- [X] T039 [P] [US2,US7] Create `tests/integration/test_task_read.py` with tests for:
  - List all tasks returns 200 with array
  - Different user's tasks are not returned (data isolation)
  - URL user_id mismatch returns 403

- [X] T040 [P] [US2,US7] Create `tests/integration/test_task_filter.py` with tests for:
  - Search by text returns matching tasks (case-insensitive)
  - Filter by status (pending/completed) works correctly
  - Filter by priority=High returns only High priority tasks
  - Filter by tags=["urgent"] returns only tasks with "urgent" tag
  - Filter by multiple tags returns tasks with ANY of the tags
  - Combine search + filters works correctly
  - Empty search/filters return all tasks

- [X] T041 [P] [US2,US7] Create `tests/integration/test_task_pagination.py` with tests for:
  - Pagination (limit, offset) works correctly
  - Sort by created_at ascending/descending works
  - Sort by due_date works
  - Sort by priority (High > Medium > Low) works
  - Sort by title alphabetically works
  - Pagination with search/filter/sort works correctly

### Implementation for User Story 2 + 7

- [X] T042 [US2,US7] Implement GET `/api/{user_id}/tasks` endpoint with all query parameters (already created in T019)
- [X] T043 [US2,US7] Implement search logic in TaskService.get_tasks():
  - Add case-insensitive ILIKE filter on title OR description
  - Use SQLModel WHERE clause with ILIKE("%search%")

- [X] T044 [US2,US7] Implement priority filter in TaskService:
  - Add WHERE clause for priority enum value
  - Handle "all" to skip filter

- [X] T045 [US2,US7] Implement tags filter in TaskService:
  - Join with task_tags and tags tables
  - Use IN clause for tag names
  - Filter by user_id on tags table (data isolation)

- [X] T046 [US2,US7] Implement sorting in TaskService:
  - Add ORDER BY clause based on sort_by parameter
  - Handle priority sorting (High=1, Medium=2, Low=3 for ascending)
  - Apply sort_direction (asc/desc)

- [X] T047 [US2] Return PaginatedResponse with data array, total, limit, offset
- [X] T048 [US2] Ensure user data isolation (only return tasks where task.user_id == JWT user_id)

**Checkpoint**: User Story 2 + 7 complete - can view, search, filter, and sort task list

---

## Phase 5: User Story 3 - Toggle Task Completion (Priority: P1)

**Goal**: Authenticated users can toggle task completion status (pending ↔ complete)

**Independent Test**: PATCH to `/api/{user_id}/tasks/{task_id}/complete` with valid JWT returns 200 with updated task

### Tests for User Story 3

- [X] T049 [P] [US3] Add tests to `tests/integration/test_task_toggle.py` for:
  - Toggle pending to complete returns 200 with completed=true
  - Toggle complete to pending returns 200 with completed=false
  - Toggle non-existent task returns 404
  - Toggle another user's task returns 403
  - Returned task includes priority, due_date, tags

### Implementation for User Story 3

- [X] T050 [US3] Implement PATCH `/api/{user_id}/tasks/{task_id}/complete` endpoint (already in T019)
- [X] T051 [US3] Implement TaskService.toggle_task_completion() method
- [X] T052 [US3] Update task.updated_at timestamp on toggle per FR-018
- [X] T053 [US3] Add proper error handling (404 for not found, 403 for unauthorized)

**Checkpoint**: User Story 3 complete - can toggle task completion status

---

## Phase 6: User Story 4 - Get Single Task (Priority: P1)

**Goal**: Authenticated users can retrieve a specific task by ID

**Independent Test**: GET to `/api/{user_id}/tasks/{task_id}` with valid JWT returns 200 with task data

### Tests for User Story 4

- [X] T054 [P] [US4] Add tests to `tests/integration/test_task_get_single.py` for:
  - Get own task returns 200 with task data including priority, due_date, tags
  - Get non-existent task returns 404
  - Get another user's task returns 403

### Implementation for User Story 4

- [X] T055 [US4] Implement GET `/api/{user_id}/tasks/{task_id}` endpoint (already in T019)
- [X] T056 [US4] Implement TaskService.get_task_by_id() method with user_id filter
- [X] T057 [US4] Return TaskResponse with all fields including priority, due_date, tags

**Checkpoint**: User Story 4 complete - can retrieve single task details

---

## Phase 7: User Story 5 - Edit Task (Priority: P2)

**Goal**: Authenticated users can update task title, description, **priority**, **due_date**, and **tags**

**Independent Test**: PUT/PATCH to `/api/{user_id}/tasks/{task_id}` with valid JWT returns 200 with updated task

### Tests for User Story 5

- [X] T058 [P] [US5] Create `tests/integration/test_task_update_delete.py` with tests for:
  - Update title returns 200 with new title
  - Update description returns 200 with new description
  - Update priority returns 200 with new priority
  - Update due_date returns 200 with new due_date
  - Update tags returns 200 with new tags (replaces existing)
  - Title > 200 chars returns 400
  - Invalid priority value returns 400
  - Update non-existent task returns 404
  - Update another user's task returns 403

### Implementation for User Story 5

- [X] T059 [US5] Implement PUT/PATCH `/api/{user_id}/tasks/{task_id}` endpoint (already in T019)
- [X] T060 [US5] Implement TaskService.update_task() method with:
  - Partial update support for all fields
  - Tag reassignment (remove old tags, add new tags)
- [X] T061 [US5] Update task.updated_at timestamp on update per FR-018
- [X] T062 [US5] Validate input using TaskUpdate schema

**Checkpoint**: User Story 5 complete - can update task details including advanced fields

---

## Phase 8: User Story 8 - Manage Tags (Priority: P2)

**Goal**: Authenticated users can view all their unique tags with usage counts for autocomplete

**Independent Test**: GET to `/api/{user_id}/tags` returns array of TagWithUsage objects

### Tests for User Story 8

- [X] T063 [P] [US8] Create `tests/integration/test_tags.py` with tests for:
  - GET /tags returns all user's unique tags with usage counts
  - Tags from different users are not returned (data isolation)
  - Usage count is accurate (counts tasks associated with each tag)
  - Empty tag list returns [] for user with no tasks
  - Tags are sorted by name alphabetically
  - Unauthenticated request returns 401
  - Wrong user_id in URL returns 403

### Implementation for User Story 8

- [X] T064 [US8] Implement TagService.get_user_tags_with_usage() (already created in T025)
- [X] T065 [US8] Implement GET `/api/{user_id}/tags` endpoint (already created in T026)
- [X] T066 [US8] Add proper error handling (401, 403)

**Checkpoint**: User Story 8 complete - can view tags with usage counts

---

## Phase 9: User Story 6 - Delete Task (Priority: P3)

**Goal**: Authenticated users can permanently delete a task (also removes tag associations via CASCADE)

**Independent Test**: DELETE to `/api/{user_id}/tasks/{task_id}` with valid JWT returns 204 No Content

### Tests for User Story 6

- [X] T067 [P] [US6] Add tests to `tests/integration/test_task_update_delete.py` for:
  - Delete own task returns 204 No Content
  - Delete non-existent task returns 404
  - Delete another user's task returns 403
  - Deleting task also removes task_tag associations (CASCADE)
  - Orphaned tags are cleaned up (no tasks reference them)

### Implementation for User Story 6

- [X] T068 [US6] Implement DELETE `/api/{user_id}/tasks/{task_id}` endpoint (already in T019)
- [X] T069 [US6] Implement TaskService.delete_task() method
- [X] T070 [US6] Return 204 No Content on successful deletion
- [X] T071 [US6] Ensure CASCADE delete removes task_tag entries automatically

**Checkpoint**: User Story 6 complete - can delete tasks

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Testing and validation for all features including advanced capabilities

- [X] T072 [P] Update `tests/contract/test_openapi_schema.py` to validate:
  - New query parameters (search, priority, tags, sort_by, sort_direction)
  - PriorityType enum schema
  - TagWithUsage schema
  - Updated Task schema with UUID id, priority, due_date, tags
  - GET /api/{user_id}/tags endpoint

- [X] T073 [P] Create `tests/unit/test_tag_service.py` to verify:
  - get_or_create_tag() creates new tags
  - get_user_tags_with_usage() returns correct counts
  - assign_tags_to_task() assigns tags correctly
  - Data isolation (user A's tags != user B's tags)

- [X] T074 [P] Create `tests/unit/test_task_search_filter.py` to verify:
  - Search query builder works correctly
  - Priority filter logic works
  - Tags filter with JOIN works
  - Sorting logic works for all fields

- [X] T075 Run `mypy src/ --strict` and fix type errors for:
  - UUID types
  - PriorityType enum
  - Optional date fields
  - List[str] tag fields

- [X] T076 [P] Run `uv run ruff check src/ --fix` for linting

- [X] T077 Run full pytest suite with coverage:
  - `uv run pytest tests/ -v --cov=src --cov-report=term-missing`
  - Ensure >80% coverage

- [X] T078 [P] Create `tests/integration/test_auth.py` with:
  - Tests for tag endpoint authentication
  - Tests for search/filter query parameter validation

**Checkpoint**: All features tested and validated

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|-----------|--------|
| Phase 1: Setup | None | Foundational |
| Phase 2: Foundational + Advanced | Setup | All User Stories |
| Phase 3: US1 Create | Foundational | US2-8 |
| Phase 4: US2 View + US7 Search/Filter | Foundational | Polish |
| Phase 5: US3 Toggle | Foundational | Polish |
| Phase 6: US4 Get Single | Foundational | Polish |
| Phase 7: US5 Edit | Foundational | Polish |
| Phase 8: US8 Manage Tags | Foundational | Polish |
| Phase 9: US6 Delete | Foundational | Polish |
| Phase 10: Polish | All US complete | - |

### User Story Dependencies

- **US1 (P1 - MVP)**: Can start after Foundational - Creates tasks with priority/due_date/tags
- **US2 (P1) + US7 (P2)**: Merged - List tasks with search/filter/sort - Uses Task/Tag models
- **US3 (P1)**: Can start after Foundational - Toggles tasks with new fields
- **US4 (P1)**: Can start after Foundational - Gets tasks with new fields
- **US5 (P2)**: Can start after Foundational - Updates tasks with new fields
- **US8 (P2)**: Can start after Foundational - Tag autocomplete endpoint
- **US6 (P3)**: Can start after Foundational - Deletes tasks with CASCADE

### Within Each User Story

- Unit tests → Contract tests → Model → Service → Endpoint → Integration tests
- Story complete before moving to next priority

---

## Parallel Opportunities

| Phase | Parallel Tasks |
|-------|----------------|
| Phase 1 | T001-T006 can run in parallel |
| Phase 2 | T007-T010, T012, T014-T017, T020-T030 can run in parallel (models/schemas/services/migrations) |
| Phase 3 | T031, T032, T033 can run in parallel (tests and implementation) |
| Phase 4 | T039, T040, T041 can run in parallel (test files for US2+US7) |
| Phase 5-9 | Each story's tests can run in parallel with implementation |
| Phase 10 | T072, T073, T074, T075, T076, T078 can run in parallel |

### Parallel Example: Phase 2 Foundational

```bash
# Run these tasks in parallel:
Task T011: Update Task model with UUID, priority, due_date
Task T022: Create Tag model
Task T023: Create TaskTag junction model
Task T013: Update TaskCreate/Update/Response schemas
Task T024: Create TagWithUsage schema
Task T025: Create TagService
Task T018: Update TaskService with search/filter/sort
Task T028-T030: Create Alembic migrations
```

---

## Implementation Strategy

### MVP First (User Story 1 Only with Advanced Features)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational + Advanced Features (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Create tasks with priority/due_date/tags)
4. **STOP and VALIDATE**: Test task creation with all new fields independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational + Advanced → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP with advanced features!)
3. Add User Story 2 + 7 → Test search/filter/sort independently → Deploy/Demo
4. Add User Story 3 → Test toggle independently → Deploy/Demo
5. Add User Story 4 → Test get single independently → Deploy/Demo
6. Add User Story 5 → Test update with advanced fields independently → Deploy/Demo
7. Add User Story 8 → Test tag autocomplete independently → Deploy/Demo
8. Add User Story 6 → Test delete independently → Deploy/Demo
9. Complete Phase 10: Polish → Final deployment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational + Advanced together
2. Once Foundational is done:
   - Developer A: User Story 1 (Create) + User Story 5 (Edit)
   - Developer B: User Story 2+7 (View/Search/Filter) + User Story 4 (Get Single)
   - Developer C: User Story 3 (Toggle) + User Story 8 (Tags) + User Story 6 (Delete)
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T006 | Setup (6 tasks) |
| Phase 2 | T007-T030 | Foundational + Advanced Features (24 tasks) |
| Phase 3 | T031-T038 | US1: Create Task with Advanced Fields (8 tasks) |
| Phase 4 | T039-T048 | US2: View + US7: Search/Filter/Sort (10 tasks) |
| Phase 5 | T049-T053 | US3: Toggle Completion (5 tasks) |
| Phase 6 | T054-T057 | US4: Get Single Task (4 tasks) |
| Phase 7 | T058-T062 | US5: Edit Task with Advanced Fields (5 tasks) |
| Phase 8 | T063-T066 | US8: Manage Tags (4 tasks) |
| Phase 9 | T067-T071 | US6: Delete Task (5 tasks) |
| Phase 10 | T072-T078 | Polish (7 tasks) |
| **Total** | **78 tasks** | All phases (integrated) |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Run `uv run pytest tests/` to validate progress
- Run `uv run mypy src/ --strict` for type safety
- **Advanced features integrated**: Priority, due_date, tags, search, filtering, sorting are now part of Phase 2 foundation and used throughout all user stories
