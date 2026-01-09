# Quickstart: FastAPI Todo Backend (Phase II)

## Prerequisites

- Python 3.13+
- uv (Python package manager)
- PostgreSQL database (Neon or local)

## Installation

### 1. Clone and Setup

```bash
cd phase-2-todo-full-stack/backend

# Install dependencies with uv
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### 2. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

#### Required Environment Variables

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@ep-xxx.region.neon.tech/dbname?sslmode=require

# Authentication (MUST match frontend BETTER_AUTH_SECRET)
BETTER_AUTH_SECRET=your-super-secret-key-minimum-32-characters

# CORS - Frontend origins
ALLOWED_ORIGINS=http://localhost:3000

# Optional: JWT validation (for production issuer/audience)
JWT_ISSUER=nextjs-frontend
JWT_AUDIENCE=fastapi-backend

# Server configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

### 3. Database Setup

```bash
# Run Alembic migrations
uv run alembic upgrade head

# Verify database connection
uv run python -c "from src.db.engine import engine; from src.models.task import Task; print('Database connected successfully')"
```

## Development

### Running the Server

```bash
# Development mode with auto-reload
uv run uvicorn src.main:app --reload --port 8000

# Or using the Python module directly
uv run python -m uvicorn src.main:app --reload --port 8000
```

### Access Points

| Endpoint | Description |
|----------|-------------|
| `http://localhost:8000` | API root (health check) |
| `http://localhost:8000/docs` | Swagger UI (interactive docs) |
| `http://localhost:8000/redoc` | ReDoc (alternative docs) |
| `http://localhost:8000/health` | Health check endpoint |

## Testing

### Run All Tests

```bash
# Run full test suite
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing
```

### Test Categories

```bash
# Unit tests (fast, no external dependencies)
uv run pytest tests/unit/ -v

# Integration tests (requires database)
uv run pytest tests/integration/ -v

# Contract tests (OpenAPI schema validation)
uv run pytest tests/contract/ -v

# Health check test
uv run pytest tests/test_health.py -v
```

### Type Checking

```bash
# Strict type checking
uv run mypy src/ --strict

# Report missing types only
uv run mypy src/ --show-error-codes
```

### Linting

```bash
# Format code
uv run ruff check src/ --fix
uv run ruff format src/

# Type checking
uv run mypy src/
```

## Production Deployment

### Docker Build

```bash
# Build Docker image
docker build -t todo-backend:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=$DATABASE_URL \
  -e BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET \
  -e ALLOWED_ORIGINS=$ALLOWED_ORIGINS \
  todo-backend:latest
```

### Environment Variables for Production

```env
# Required
DATABASE_URL=postgresql://...  # Neon connection string
BETTER_AUTH_SECRET=<32+ chars> # Same as frontend

# Recommended for production
DEBUG=false
ALLOWED_ORIGINS=https://your-domain.com
```

### Docker Compose (with frontend)

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/todo
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - ALLOWED_ORIGINS=http://frontend:3000
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - NEXT_PUBLIC_API_URL=http://backend:8000

  db:
    image: postgres:15-alpine
    # Or use Neon external database
```

## Verification Checklist

- [ ] Dependencies installed (`uv sync`)
- [ ] Environment variables configured (`.env` file)
- [ ] Database migrations applied (`alembic upgrade head`)
- [ ] Server starts without errors (`uv run uvicorn src.main:app`)
- [ ] Health endpoint responds (`curl http://localhost:8000/health`)
- [ ] Swagger docs accessible (`http://localhost:8000/docs`)
- [ ] Unit tests pass (`uv run pytest tests/unit/`)
- [ ] Type checking passes (`uv run mypy src/ --strict`)

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
uv run python -c "
from sqlalchemy import create_engine
engine = create_engine('$DATABASE_URL')
with engine.connect() as conn:
    print('Database connected!')
"
```

### JWT Validation Errors

Ensure `BETTER_AUTH_SECRET` matches exactly between frontend and backend:
```bash
# Verify secrets match
echo "Frontend: $BETTER_AUTH_SECRET"
echo "Backend:  $BETTER_AUTH_SECRET"
```

### CORS Errors

Add your origin to `ALLOWED_ORIGINS` in `.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
```
