# Backend - Phase 4 Kubernetes Deployment

## Overview
FastAPI backend with AI-powered ChatKit server deployed to Kubernetes using Docker with Helm chart management.

## Tech Stack
- **Framework:** FastAPI 0.115+
- **Language:** Python 3.13+
- **Package Manager:** UV (fast Python package installer)
- **Database:** Neon Serverless PostgreSQL (asyncpg driver)
- **ORM:** SQLModel (sync) + SQLAlchemy async (for health checks)
- **AI/LLM:** Multi-provider support (OpenAI, Gemini, Groq, OpenRouter)
- **Auth:** JWT validation with shared secret (Better Auth compatible)
- **Deployment:** Docker + Kubernetes + Helm

## Critical Kubernetes Fixes

### 1. asyncpg SSL Configuration
**Problem:** Database connection failed with error:
```
connect() got an unexpected keyword argument 'sslmode'
```

**Root Cause:** The DATABASE_URL contains `?sslmode=require` which works for psycopg2 (sync driver) but not for asyncpg (async driver). asyncpg doesn't support `sslmode` as a URL parameter.

**Solution:** Modified `src/db/async_session.py` to:
1. Remove `sslmode` parameter from URL
2. Configure SSL via `connect_args`

```python
# Remove sslmode query parameter if present
async_database_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)
if "?sslmode=" in async_database_url:
    async_database_url = async_database_url.split("?sslmode=")[0]
elif "&sslmode=" in async_database_url:
    async_database_url = async_database_url.split("&sslmode=")[0]

async_engine = create_async_engine(
    async_database_url,
    echo=settings.ENVIRONMENT == "development",
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    pool_recycle=settings.DB_POOL_RECYCLE,
    connect_args={
        "ssl": "require",  # asyncpg SSL configuration
        "server_settings": {
            "application_name": "todo-app",
        },
    },
)
```

**Why This Matters:** The readiness probe uses async database connection to verify database connectivity. Without this fix, the backend pod never becomes ready, causing deployment failure.

### 2. LLM Provider Configuration
**Problem:** ChatKit endpoint returned 500 errors:
```
ValueError: OPENAI_API_KEY environment variable is required when LLM_PROVIDER=openai
```

**Root Cause:** ConfigMap was set to `LLM_PROVIDER=openai` but only `OPENROUTER_API_KEY` was available in Secrets.

**Solution:** Updated ConfigMap to use the correct provider:
```bash
kubectl patch configmap -n todo-app todo-app-config --type merge -p '{"data":{"LLM_PROVIDER":"openrouter"}}'
```

**Configuration Options:**
- `openai` - Requires `OPENAI_API_KEY`
- `openrouter` - Requires `OPENROUTER_API_KEY`
- `groq` - Requires `GROQ_API_KEY`
- `gemini` - Requires `GEMINI_API_KEY`

**Important:** Always ensure the `LLM_PROVIDER` matches the available API key in your Secrets.

### 3. Health and Readiness Endpoints
**Purpose:** Kubernetes uses these endpoints to determine pod health and readiness.

**Liveness Probe (`/api/health`):**
- Simple health check
- Returns 200 OK if service is running
- Kubernetes restarts pod if this fails

**Readiness Probe (`/api/ready`):**
- Comprehensive readiness check
- Validates:
  - Required environment variables (DATABASE_URL, BETTER_AUTH_SECRET)
  - At least one LLM API key is present
  - Database connectivity (async connection test)
- Returns 200 OK only when all checks pass
- Kubernetes routes traffic only to ready pods

**Implementation:** `src/api/health.py`
```python
@router.get("/ready")
async def readiness_check():
    checks = {
        "environment": "ok",
        "database": "ok"
    }
    errors = []

    # Check required environment variables
    if not os.getenv("DATABASE_URL"):
        checks["environment"] = "failed"
        errors.append("Missing required environment variable: DATABASE_URL")

    # Check at least one LLM API key
    llm_keys = ["OPENAI_API_KEY", "OPENROUTER_API_KEY", "GROQ_API_KEY", "GEMINI_API_KEY"]
    if not any(os.getenv(key) for key in llm_keys):
        checks["environment"] = "failed"
        errors.append("At least one LLM API key is required")

    # Check database connectivity
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            result.scalar()
    except Exception as e:
        checks["database"] = "failed"
        errors.append(f"Database connection failed: {str(e)}")

    if errors:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "checks": checks,
                "errors": errors
            }
        )

    return {
        "status": "ready",
        "service": "backend",
        "checks": checks
    }
```

### 4. Port Configuration
**Port:** 8001 (not 8000)

**Reason:** Port 8000 was already in use by another application on the host system.

**Configuration:**
- Dockerfile: `EXPOSE 8001`
- Kubernetes Service: `port: 8001`
- ConfigMap: `BACKEND_URL: http://todo-app-backend:8001`
- Frontend rewrites: Point to port 8001

## Docker Configuration

### Multi-Stage Dockerfile with UV
```dockerfile
# Stage 1: Builder
FROM python:3.13-slim AS builder
WORKDIR /app

# Install UV package manager from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies
RUN apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Increase UV timeout for slow networks
ENV UV_HTTP_TIMEOUT=300

# Install dependencies
RUN uv sync --frozen --no-dev

# Stage 2: Runner
FROM python:3.13-slim AS runner
WORKDIR /app

# Install runtime dependencies
RUN apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY mcp_server/ ./mcp_server/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8001

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

# Run migrations and start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8001"]
```

**Key Points:**
- Uses official UV image for fast dependency installation
- Multi-stage build reduces final image size
- Non-root user (UID 1000) for security
- Runs Alembic migrations on startup
- Increased UV timeout (300s) for slow networks
- APT repository expiration fix with `-o Acquire::Check-Valid-Until=false`

## Kubernetes Configuration

### Deployment
- **Image:** `todo-backend:latest` (built in Minikube Docker daemon)
- **Port:** 8001
- **Replicas:** 1
- **Security:** Non-root user (UID 1000)
- **Health Probes:**
  - Liveness: `/api/health` (every 10s)
  - Readiness: `/api/ready` (every 10s, initial delay 10s)

### Service
- **Type:** ClusterIP (internal only)
- **Port:** 8001
- **Purpose:** Internal communication from frontend

### Environment Variables

**From ConfigMap:**
- `LLM_PROVIDER`: `openrouter` (or `openai`, `groq`, `gemini`)
- `OPENAI_DEFAULT_MODEL`: `gpt-4o-mini`
- `OPENROUTER_DEFAULT_MODEL`: `openai/gpt-4o-mini`
- `GROQ_DEFAULT_MODEL`: `llama-3.3-70b-versatile`
- `GEMINI_DEFAULT_MODEL`: `gemini-2.5-flash`
- `LOG_LEVEL`: `debug` (or `info`, `warning`, `error`)

**From Secrets:**
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret for JWT validation
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `OPENROUTER_API_KEY`: OpenRouter API key (optional)
- `GROQ_API_KEY`: Groq API key (optional)
- `GEMINI_API_KEY`: Gemini API key (optional)

**Important:** At least one LLM API key must be provided, and `LLM_PROVIDER` must match an available key.

## Access Methods

### Internal (from Frontend)
```
http://todo-app-backend:8001
```

### Port-Forwarding (for testing)
```bash
# Backend (keep running in separate terminal)
kubectl port-forward svc/todo-app-backend 8001:8001 -n todo-app --address 0.0.0.0

# Test from Windows/WSL2
curl http://localhost:8001/api/health
curl http://localhost:8001/api/ready
```

## Common Issues

### Issue 1: Readiness Probe Failing with 503
**Symptom:** Pod shows `0/1 Running` and never becomes ready.

**Possible Causes:**
1. **Missing API Key:** No LLM API key provided
   - Check: `kubectl logs -n todo-app -l app.kubernetes.io/component=backend | grep "API_KEY"`
   - Fix: Ensure at least one API key is in Secrets

2. **Wrong LLM Provider:** `LLM_PROVIDER` doesn't match available API key
   - Check: `kubectl get configmap -n todo-app todo-app-config -o yaml | grep LLM_PROVIDER`
   - Fix: Update ConfigMap to match your API key

3. **Database Connection Failed:** asyncpg SSL configuration issue
   - Check: `kubectl logs -n todo-app -l app.kubernetes.io/component=backend | grep "sslmode"`
   - Fix: Ensure `src/db/async_session.py` has the SSL fix

### Issue 2: ChatKit 500 Errors
**Symptom:** Frontend shows ChatKit errors, backend logs show:
```
ValueError: OPENAI_API_KEY environment variable is required when LLM_PROVIDER=openai
```

**Solution:**
```bash
# Check current provider
kubectl get configmap -n todo-app todo-app-config -o yaml | grep LLM_PROVIDER

# Update to match your API key
kubectl patch configmap -n todo-app todo-app-config --type merge -p '{"data":{"LLM_PROVIDER":"openrouter"}}'

# Restart backend
kubectl rollout restart deployment -n todo-app todo-app-backend
```

### Issue 3: Database Connection Timeout
**Symptom:** Readiness probe fails with database timeout.

**Possible Causes:**
1. Invalid DATABASE_URL
2. Network connectivity issues
3. Neon database not accessible from cluster

**Debug:**
```bash
# Check database URL (masked)
kubectl exec -n todo-app <backend-pod> -- sh -c 'echo $DATABASE_URL | sed "s/:.*@/:***@/"'

# Test database connectivity
kubectl exec -n todo-app <backend-pod> -- sh -c 'python -c "import asyncpg; import asyncio; asyncio.run(asyncpg.connect(\"$DATABASE_URL\"))"'
```

## Build and Deploy

### Build Docker Image
```bash
# Use Minikube Docker daemon
eval $(minikube docker-env)

# Build image
docker build -t todo-backend:latest -f backend/Dockerfile backend/
```

### Deploy with Helm
```bash
# Deploy or upgrade
helm upgrade --install todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-dev.yaml \
  -n todo-app \
  --set secrets.DATABASE_URL="$DATABASE_URL" \
  --set secrets.BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  --set secrets.OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
  --set config.LLM_PROVIDER="openrouter"
```

### Restart Deployment
```bash
# After code changes and rebuild
kubectl rollout restart deployment -n todo-app todo-app-backend
```

## Monitoring

### Check Logs
```bash
# Follow logs
kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f

# Check for errors
kubectl logs -n todo-app -l app.kubernetes.io/component=backend --tail=100 | grep -i error

# Check ChatKit requests
kubectl logs -n todo-app -l app.kubernetes.io/component=backend | grep -i chatkit
```

### Check Pod Status
```bash
kubectl get pods -n todo-app
kubectl describe pod -n todo-app <pod-name>
```

### Test Endpoints
```bash
# Health check
curl http://localhost:8001/api/health

# Readiness check (detailed)
curl http://localhost:8001/api/ready

# API root
curl http://localhost:8001/
```

## Key Files
- `src/db/async_session.py` - Async database session with SSL fix (critical)
- `src/api/health.py` - Health and readiness endpoints
- `src/api/v1/chatkit.py` - ChatKit endpoint
- `src/agent_config/factory.py` - LLM provider factory
- `src/main.py` - FastAPI application entry point
- `Dockerfile` - Multi-stage Docker build with UV
- `alembic/` - Database migrations

## Environment Variables

### Required
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Shared secret for JWT validation
- At least one of:
  - `OPENAI_API_KEY`
  - `OPENROUTER_API_KEY`
  - `GROQ_API_KEY`
  - `GEMINI_API_KEY`

### Optional
- `LLM_PROVIDER` - Default: `openai` (must match available API key)
- `LOG_LEVEL` - Default: `info`
- `DB_POOL_SIZE` - Default: `5`
- `DB_MAX_OVERFLOW` - Default: `10`
- `DB_POOL_RECYCLE` - Default: `300` (seconds)

## Database Configuration

### Sync Engine (SQLModel)
Used for:
- Task CRUD operations
- Alembic migrations
- Synchronous API endpoints

### Async Engine (SQLAlchemy + asyncpg)
Used for:
- ChatKit server operations
- Health/readiness checks
- Async API endpoints

**Important:** Both engines connect to the same database but use different drivers:
- Sync: psycopg2 (supports `sslmode` in URL)
- Async: asyncpg (requires `ssl` in `connect_args`)

## Security

### Non-Root User
- Container runs as UID 1000 (appuser)
- No privilege escalation
- Read-only root filesystem (where possible)

### Secrets Management
- All sensitive data in Kubernetes Secrets
- Never commit secrets to git
- Use `.env` file locally (gitignored)

### Network Policies
- Backend service is ClusterIP (internal only)
- Only frontend can access backend
- No direct external access to backend

## Performance

### Connection Pooling
- Pool size: 5 connections
- Max overflow: 10 connections
- Pool recycle: 300 seconds
- Pre-ping enabled for connection health checks

### Resource Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Troubleshooting

### Pod Stuck in CrashLoopBackOff
1. Check logs: `kubectl logs -n todo-app <pod-name>`
2. Check events: `kubectl describe pod -n todo-app <pod-name>`
3. Common causes:
   - Missing environment variables
   - Database connection failed
   - Alembic migration failed

### Readiness Probe Never Passes
1. Check readiness endpoint: `kubectl port-forward -n todo-app <pod-name> 8001:8001` then `curl http://localhost:8001/api/ready`
2. Check logs for specific error
3. Verify all required environment variables are set
4. Test database connectivity

### ChatKit Not Working
1. Check LLM_PROVIDER matches available API key
2. Check backend logs for ChatKit requests
3. Verify frontend proxy route is working
4. Test backend endpoint directly: `curl -X POST http://localhost:8001/api/chatkit -H "Authorization: Bearer <token>"`
