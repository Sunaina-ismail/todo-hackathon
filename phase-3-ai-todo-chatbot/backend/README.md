# Todo API Backend - Phase 2

Production-Ready FastAPI backend for the Todo application with JWT authentication using Better Auth shared secret approach and Neon Serverless PostgreSQL.

## Features

- RESTful API endpoints for task management
- JWT authentication with shared secret between Next.js and FastAPI
- User isolation - each user can only access their own tasks
- Neon Serverless PostgreSQL integration with optimized connection pooling
- Complete CRUD operations for tasks
- SQLModel ORM with type safety
- Alembic database migrations
- Comprehensive test suite (unit, integration, contract)

## Technology Stack

- **Framework**: FastAPI 0.115+
- **Language**: Python 3.13+
- **ORM**: SQLModel 0.0.22+
- **Database**: Neon Serverless PostgreSQL
- **Auth**: python-jose (JWT with HS256)
- **Migrations**: Alembic 1.13+
- **Package Manager**: UV (fast pip replacement)
- **Testing**: pytest with async support

## API Endpoints

All endpoints require JWT token in `Authorization: Bearer <token>` header.

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/health` | Health check (no auth) | 200 |
| `POST` | `/api/{user_id}/tasks` | Create new task | 201, 400, 401, 403 |
| `GET` | `/api/{user_id}/tasks` | List tasks (with filters) | 200, 401, 403 |
| `GET` | `/api/{user_id}/tasks/{task_id}` | Get specific task | 200, 401, 403, 404 |
| `PUT` | `/api/{user_id}/tasks/{task_id}` | Update task | 200, 400, 401, 403, 404 |
| `DELETE` | `/api/{user_id}/tasks/{task_id}` | Delete task | 204, 401, 403, 404 |
| `PATCH` | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion | 200, 401, 403, 404 |

### Query Parameters (GET /api/{user_id}/tasks)

- `completed` (boolean, optional): Filter by completion status
- `limit` (integer, default=50, max=100): Number of tasks to return
- `offset` (integer, default=0): Pagination offset

## Setup Instructions

### Prerequisites

- Python 3.13+
- UV package manager
- Neon PostgreSQL database
- Matching BETTER_AUTH_SECRET with Next.js frontend

### Installation

1. **Install dependencies**:
   ```bash
   cd phase-2-todo-full-stack/backend
   uv sync
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   #   - DATABASE_URL (from Neon console)
   #   - BETTER_AUTH_SECRET (must match frontend)
   #   - ALLOWED_ORIGINS (Next.js URL)
   ```

3. **Run database migrations**:
   ```bash
   uv run alembic upgrade head
   ```

4. **Start development server**:
   ```bash
   uv run uvicorn src.main:app --reload --port 8000
   ```

5. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/integration/test_task_create.py

# Run with verbose output
uv run pytest -v
```

### Type Checking

```bash
# Run mypy strict type checking
uv run mypy src/ --strict
```

### Linting

```bash
# Run ruff linter and auto-fix
uv run ruff check src/ --fix

# Format code
uv run ruff format src/
```

### Database Migrations

```bash
# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# View migration history
uv run alembic history
```

## Docker

### Build and Run

```bash
# Build image
docker build -t todo-backend .

# Run container
docker run -p 8000:8000 --env-file .env todo-backend

# Using docker-compose
docker-compose up --build
```

## Security

- **JWT Validation**: All endpoints (except /health) require valid JWT token
- **User Isolation**: URL user_id must match JWT sub claim
- **Data Filtering**: All queries filter by authenticated user's ID
- **CORS**: Only configured origins allowed
- **SSL/TLS**: Required for Neon connections
- **Environment Variables**: Secrets stored securely in .env

## Architecture

### Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings with pydantic-settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── tasks.py        # Task CRUD endpoints
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # JWT dependencies
│   │   └── jwt.py              # JWT validation
│   ├── db/
│   │   ├── __init__.py
│   │   ├── engine.py           # SQLModel engine
│   │   └── session.py          # Session dependency
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # SQLModel base
│   │   └── task.py             # Task entity
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py             # Task schemas
│   │   └── common.py           # Common schemas
│   └── services/
│       ├── __init__.py
│       ├── task_service.py     # Business logic
│       └── exceptions.py       # Custom exceptions
├── tests/                      # Test suite
├── alembic/                    # Database migrations
├── .env.example               # Example environment variables
├── pyproject.toml             # Project configuration
├── Dockerfile                 # Docker configuration
└── README.md                  # This file
```

### Authentication Flow

1. User authenticates with Better Auth in Next.js
2. Better Auth creates session and issues JWT token
3. Next.js sends JWT in `Authorization: Bearer <token>` header
4. FastAPI validates JWT signature using shared BETTER_AUTH_SECRET
5. FastAPI extracts user_id from JWT 'sub' claim
6. FastAPI validates URL user_id matches JWT user_id
7. FastAPI filters all data by authenticated user_id

### Database Schema

**Task Table**:
- `id` (integer, primary key)
- `user_id` (text, indexed, foreign key)
- `title` (text, 1-200 chars, required)
- `description` (text, 0-1000 chars, optional)
- `completed` (boolean, default false)
- `created_at` (timestamp)
- `updated_at` (timestamp)

## Performance

- **Connection Pooling**: Optimized for Neon Serverless
  - pool_size=5
  - max_overflow=10
  - pool_pre_ping=True (critical for serverless)
  - pool_recycle=300 (5 minutes)
- **Statement Timeout**: 30 seconds
- **Async Support**: All endpoints use async/await
- **Indexing**: user_id and created_at fields indexed

## Troubleshooting

### Database Connection Issues
1. Verify DATABASE_URL in .env
2. Check Neon project is running
3. Confirm SSL mode is 'require'
4. Test connection: `uv run python -c "from src.db.engine import engine; print(engine)"`

### Authentication Failures
1. Verify BETTER_AUTH_SECRET matches frontend
2. Check JWT token format in Authorization header
3. Confirm user_id in URL matches JWT sub claim
4. Review logs for specific error messages

### Migration Issues
1. Check DATABASE_URL is correct
2. Verify alembic.ini configuration
3. Review migration files in alembic/versions/
4. Check database connection permissions

## Contributing

1. Create feature branch from main
2. Follow code style (ruff, mypy)
3. Write tests for new features
4. Ensure all tests pass
5. Update documentation
6. Submit pull request

## License

MIT
