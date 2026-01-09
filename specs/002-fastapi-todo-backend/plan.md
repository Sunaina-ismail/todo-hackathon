# Implementation Plan: FastAPI Todo Backend (Phase II)

**Branch**: `002-fastapi-todo-backend` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification for Production-Ready FastAPI Backend with JWT authentication and Neon PostgreSQL

## Summary

Production-Ready FastAPI Backend for Todo App (Phase II) - A secure, multi-tenant REST API that validates user identity via JWT tokens from Better Auth and provides strictly isolated data access per user. Uses SQLModel ORM with Neon PostgreSQL, connection pooling for serverless, and CORS configured for Next.js frontend.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, python-jose (JWT), alembic (migrations), psycopg2-binary/postgres (Neon)
**Storage**: Neon PostgreSQL with SQLModel ORM and connection pooling
**Testing**: pytest with API integration tests, unit tests for JWT validation, contract tests for OpenAPI schema
**Target Platform**: Linux server (containerized for Docker/Kubernetes)
**Project Type**: web-backend (FastAPI service with separate frontend)
**Performance Goals**: Support 1000 concurrent users, 95% responses under 1 second
**Constraints**: Stateless (no session state), JWT validation on every request, user_id URL must match JWT sub claim
**Scale/Scope**: Single-tenant per user, strict data isolation enforced at API level

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status | Evidence |
|------|-------------|--------|----------|
| **Type Safety** | `mypy --strict` for Python | ✅ PASS | Python 3.13+, type hints required by constitution |
| **Explicit Error Handling** | Structured, descriptive errors | ✅ PASS | FR-012, FR-019 require error handling |
| **12-Factor Alignment** | Config via env, stateless, backing services | ✅ PASS | Environment variables, connection pooling |
| **No Placeholder Logic** | Full implementation required | ✅ PASS | All 6 user stories to be implemented |
| **Automated Testing** | API integration tests for all endpoints | ✅ PASS | Reference code has comprehensive test suite |
| **JWT Auth Tests** | Verify auth and user isolation | ✅ PASS | FR-001 to FR-004 mandate auth testing |
| **Sub-Agents/Skills** | Must follow constitution | ✅ PASS | Using better-auth and fastapi-development skills |

**Constitution Check Result**: ✅ PASSED - All gates satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/002-fastapi-todo-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # NOT NEEDED - spec is complete, no clarifications required
├── data-model.md        # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
├── contracts/           # Phase 1 output (below)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (phase-2-todo-full-stack/backend/)

Following reference code structure from `reference-code-uneeza/backend/`:

```text
phase-2-todo-full-stack/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_create_tasks_table.py
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Settings via pydantic-settings
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       └── tasks.py           # Task CRUD endpoints
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py        # JWT dependency (get_current_user)
│   │   │   └── jwt.py                 # JWT validation functions
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py              # SQLModel engine with pooling
│   │   │   └── session.py             # Session dependency
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # SQLModel base class
│   │   │   ├── task.py                # Task entity (UUID, priority, due_date)
│   │   │   ├── tag.py                 # Tag entity (user-specific tags)
│   │   │   └── task_tag.py            # TaskTag junction table (many-to-many)
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── task.py                # Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse)
│   │   │   └── common.py              # Common response schemas
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── task_service.py        # Task business logic (CRUD, search, filter, sort)
│   │       ├── tag_service.py         # Tag business logic (autocomplete, usage counts)
│   │       └── exceptions.py          # Custom exceptions
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── __init__.py
│   │   │   ├── test_jwt_validation.py
│   │   │   ├── test_models.py
│   │   │   └── test_task_service.py
│   │   ├── integration/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_task_create.py
│   │   │   ├── test_task_read.py
│   │   │   ├── test_task_update_delete.py
│   │   │   ├── test_task_filter.py
│   │   │   └── test_task_pagination.py
│   │   ├── contract/
│   │   │   ├── __init__.py
│   │   │   └── test_openapi_schema.py
│   │   ├── generate_token.py          # Helper for test JWT generation
│   │   └── test_health.py
│   ├── .env                           # Environment variables
│   ├── .env.example
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── Dockerfile
│   └── README.md
└── frontend/                          # Next.js 16 (separate plan/spec)
```

**Structure Decision**: Using `phase-2-todo-full-stack/` as the root for Phase 2 implementation, with `backend/` subdirectory for FastAPI service. Backend structure mirrors reference code exactly with:
- `src/api/v1/` for API endpoints
- `src/auth/` for JWT validation
- `src/db/` for SQLModel engine and sessions
- `src/models/` for SQLModel entities
- `src/schemas/` for Pydantic request/response models
- `src/services/` for business logic
- `alembic/` for database migrations
- Comprehensive test structure (unit, integration, contract)

## Phase 0: Research

**Status**: NOT NEEDED - All technical decisions are clear from spec and reference code.

| Decision | Rationale | Source |
|----------|-----------|--------|
| JWT validation with HS256 | Symmetric signing with shared BETTER_AUTH_SECRET | spec.md FR-001, reference code |
| User ID from JWT 'sub' claim | Better Auth issues tokens with user ID in 'sub' | reference code, better-auth skill |
| URL user_id validation | Enforce strict user data isolation | spec.md FR-002 |
| SQLModel for ORM | Type-safe ORM with Pydantic integration | constitution mandates, reference code |
| Neon connection pooling | Serverless-optimized with pool_pre_ping | spec.md FR-014 |
| Alembic for migrations | Production-ready migration tool | reference code |
| Pydantic v2 for validation | Current standard, integrated with FastAPI | reference code |

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

**Task Entity** (SQLModel):
```python
from enum import Enum
import uuid
from datetime import date

class PriorityType(str, Enum):
    High = "High"
    Medium = "Medium"
    Low = "Low"

class Task(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False)  # Better Auth UUID
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: PriorityType = Field(default=PriorityType.Medium)  # NEW
    due_date: date | None = Field(default=None)  # NEW
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, onupdate=datetime.utcnow)
```

**Tag Entity** (SQLModel):
```python
class Tag(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    user_id: str = Field(index=True, nullable=False)  # User-specific tags
```

**TaskTag Junction Table** (SQLModel):
```python
class TaskTag(SQLModel, table=True):
    task_id: uuid.UUID = Field(foreign_key="tasks.id", primary_key=True, ondelete="CASCADE")
    tag_id: uuid.UUID = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")
```

**Pydantic Schemas**:
- `TaskCreate`: title (1-200), description (0-1000, optional), priority (High/Medium/Low, default: Medium), due_date (optional ISO date), tags (list of strings)
- `TaskUpdate`: title (optional), description (optional), completed (optional), priority (optional), due_date (optional), tags (optional list replaces existing)
- `TaskResponse`: All Task fields with datetime/date serialization, tags (list of strings)
- `TagWithUsage`: name (string), usage_count (int) - for autocomplete

### API Contracts (`contracts/openapi.yaml`)

**Base Path**: `/api/{user_id}/tasks`

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/api/{user_id}/tasks` | Create task (with priority, due_date, tags) | 201, 400, 401, 403 |
| `GET` | `/api/{user_id}/tasks` | List tasks (?search=&status=&priority=&tags[]=&sort_by=&sort_direction=&limit=&offset=) | 200, 401, 403 |
| `GET` | `/api/{user_id}/tasks/{task_id}` | Get single task | 200, 401, 403, 404 |
| `PUT/PATCH` | `/api/{user_id}/tasks/{task_id}` | Update task (priority, due_date, tags supported) | 200, 400, 401, 403, 404 |
| `DELETE` | `/api/{user_id}/tasks/{task_id}` | Delete task | 204, 401, 403, 404 |
| `PATCH` | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion | 200, 401, 403, 404 |
| `GET` | `/api/{user_id}/tags` | Get user's unique tags with usage counts | 200, 401, 403 |

**Query Parameters for GET /tasks**:
- `search` (string): Full-text search in title/description
- `status` (string): `all` | `pending` | `completed` (default: all)
- `priority` (string): `all` | `High` | `Medium` | `Low` (default: all)
- `tags` (array): Filter by one or more tag names (e.g., `?tags[]=urgent&tags[]=work`)
- `sort_by` (string): `created_at` | `updated_at` | `title` | `due_date` | `priority` (default: created_at)
- `sort_direction` (string): `asc` | `desc` (default: desc)
- `limit` (int): Max results (1-100, default: 50)
- `offset` (int): Skip N results (default: 0)

**Security Scheme**: Bearer token (JWT) in `Authorization: Bearer <token>` header

### Quickstart (`quickstart.md`)

```bash
# Setup
cd phase-2-todo-full-stack/backend
uv sync

# Environment
cp .env.example .env
# Edit .env with:
#   DATABASE_URL=postgresql://user:pass@host/db
#   BETTER_AUTH_SECRET=<same as frontend>
#   ALLOWED_ORIGINS=http://localhost:3000

# Run migrations
uv run alembic upgrade head

# Start server
uv run uvicorn src.main:app --reload --port 8000

# Tests
uv run pytest tests/
uv run pytest tests/integration/
uv run pytest tests/unit/
uv run mypy src/
```

### Generated Artifacts

| File | Description |
|------|-------------|
| `data-model.md` | Entity definitions and validation rules |
| `contracts/openapi.yaml` | OpenAPI 3.1 schema for all endpoints |
| `quickstart.md` | Setup and run instructions |

## Key Design Decisions

### 1. JWT Validation Strategy
**Decision**: Use python-jose with HS256 algorithm, validate issuer/audience for production
**Rationale**: Matches Better Auth JWT plugin, enables secure token verification
**Alternatives**: PyJWT (rejected - less feature-rich for issuer/audience validation)

### 2. Database Session Management
**Decision**: SQLModel with async support, connection pooling (pool_size=5, max_overflow=10)
**Rationale**: Neon serverless requires connection recycling, pool_pre_ping prevents stale connections
**Alternatives**: Plain SQLAlchemy (rejected - SQLModel provides better type safety)

### 3. API Structure
**Decision**: RESTful with `/api/{user_id}/tasks` pattern, validate URL user_id matches JWT sub
**Rationale**: Explicit user isolation at API level, prevents any accidental data leakage
**Alternatives**: Sub-resources under user (rejected - URL user_id validation is clearer)

### 4. Error Handling
**Decision**: Custom exception handlers, structured JSON errors with detail field
**Rationale**: FR-012, FR-019 require clear, actionable error messages
**Format**: `{"detail": "error message"}` for HTTPException, validation errors as array

### 5. CORS Configuration
**Decision**: Allow credentials, specific origins (no wildcard), Authorization header exposed
**Rationale**: Next.js frontend needs Authorization header, cookies for auth state
**Origins**: From environment variable (localhost:3000 for dev, production URL for prod)

### 6. Task ID Type (UUID vs Integer)
**Decision**: Use UUID (uuid4) as primary key for tasks instead of auto-incrementing integers
**Rationale**: Better security (prevents ID enumeration attacks), globally unique identifiers, matches reference implementation
**Alternatives**: Auto-increment integers (rejected - predictable IDs enable enumeration)

### 7. Tag System Architecture
**Decision**: Many-to-many relationship with junction table (task_tags), user-specific tags
**Rationale**: Users can have multiple tasks per tag and multiple tags per task, strict data isolation per user
**Constraints**: Tag names unique per user (composite index on user_id + name), cascade delete when task deleted
**Alternatives**: Simple tag field as JSON array (rejected - no query optimization, no autocomplete)

### 8. Priority Levels Enum
**Decision**: Store priority as string enum (High/Medium/Low) with default value of Medium
**Rationale**: Limited, well-defined values prevent invalid data, sortable by enum order
**Alternatives**: Integer scale 1-5 (rejected - less semantic, harder to understand)

### 9. Search and Filtering Strategy
**Decision**: Case-insensitive full-text search on title/description, separate filters for priority/tags/status
**Rationale**: Users need to find tasks quickly in large lists, multiple filter criteria combinable
**Implementation**: SQLModel WHERE clauses with ILIKE for search, IN for tags, equality for priority/status
**Alternatives**: Full-text search index (rejected - overkill for Phase 2, can add later if needed)

### 10. Sort Implementation
**Decision**: Support sorting by created_at, updated_at, title, due_date, priority with asc/desc direction
**Rationale**: Users need different views (newest first, by deadline, by priority), multiple sort fields enable flexible UX
**Default**: created_at DESC (newest first)
**Priority Order**: High > Medium > Low (for ascending sort)

## Complexity Tracking

> No constitutional violations requiring justification. All design decisions align with constitution requirements.

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks from this plan
2. Implement backend in `phase-2-todo-full-stack/backend/`
3. Create unit tests for JWT validation (`tests/unit/test_jwt_validation.py`)
4. Create integration tests for all endpoints (`tests/integration/`)
5. Verify with `mypy --strict` and `pytest`
