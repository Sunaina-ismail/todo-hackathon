# Quickstart Guide: AI-Powered Conversational Task Management

**Feature**: 004-ai-chatbot
**Date**: 2026-01-12
**Phase**: Phase 1 - Development Setup

## Overview

This guide provides step-by-step instructions for setting up the development environment and implementing the AI-powered conversational task management feature. Follow these steps to get the chatbot running locally.

---

## Prerequisites

### Required Software

- **Python**: 3.13+ (backend)
- **Node.js**: 18+ (frontend)
- **UV**: Latest version (Python package manager)
- **PostgreSQL**: Neon Serverless (cloud database)
- **Git**: For version control

### Required Accounts

- **Neon**: PostgreSQL database (https://neon.tech)
- **OpenAI**: API key (https://platform.openai.com) OR
- **Gemini**: API key (https://ai.google.dev) OR
- **Groq**: API key (https://console.groq.com) OR
- **OpenRouter**: API key (https://openrouter.ai) - has free tier

### Existing Phase II Setup

This feature builds on Phase II. Ensure Phase II is working:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Database migrations applied
- ✅ Better Auth configured
- ✅ JWT authentication working

---

## Step 1: Environment Configuration

### Backend Environment Variables

Create or update `phase-3-ai-todo-chatbot/backend/.env`:

```bash
# Existing Phase II variables
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-must-match-frontend
CORS_ORIGINS=http://localhost:3000

# NEW: LLM Provider Configuration (choose one)
LLM_PROVIDER=openai  # openai | gemini | groq | openrouter

# NEW: OpenAI Configuration (if LLM_PROVIDER=openai)
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# NEW: Gemini Configuration (if LLM_PROVIDER=gemini)
# GEMINI_API_KEY=AIza...
# GEMINI_DEFAULT_MODEL=gemini-2.5-flash

# NEW: Groq Configuration (if LLM_PROVIDER=groq)
# GROQ_API_KEY=gsk_...
# GROQ_DEFAULT_MODEL=llama-3.3-70b-versatile

# NEW: OpenRouter Configuration (if LLM_PROVIDER=openrouter)
# OPENROUTER_API_KEY=sk-or-v1-...
# OPENROUTER_DEFAULT_MODEL=openai/gpt-oss-20b:free

# NEW: MCP Server Configuration
MCP_SERVER_NAME=todo-task-server
```

### Frontend Environment Variables

Create or update `phase-3-ai-todo-chatbot/frontend/.env.local`:

```bash
# Existing Phase II variables
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-must-match-backend
BETTER_AUTH_URL=http://localhost:3000

# Existing Phase II variables
NEXT_PUBLIC_API_URL=http://localhost:8000

# NEW: ChatKit Configuration
NEXT_PUBLIC_CHATKIT_URL=http://localhost:8000/api/chatkit
```

**IMPORTANT**: `BETTER_AUTH_SECRET` must be identical in both backend and frontend `.env` files.

---

## Step 2: Install Dependencies

### Backend Dependencies

```bash
cd phase-3-ai-todo-chatbot/backend

# Install Phase 3 dependencies
uv sync

# Verify installation
uv run python -c "import agents; import mcp; import chatkit; print('Dependencies OK')"
```

**New Dependencies Added**:
- `openai-agents>=0.2.9` - OpenAI Agents SDK
- `mcp>=1.0.0` - Official MCP Python SDK (FastMCP)
- `openai-chatkit>=0.1.0` - ChatKit Python server
- `openai>=1.0.0` - OpenAI client (for multi-provider support)
- `sse-starlette>=2.0.0` - SSE streaming support
- `nest-asyncio>=1.6.0` - Async event loop support

### Frontend Dependencies

```bash
cd phase-3-ai-todo-chatbot/frontend

# Install Phase 3 dependencies
npm install

# Verify installation
npm list @openai/chatkit-react
```

**New Dependencies Added**:
- `@openai/chatkit-react` - ChatKit React components

---

## Step 3: Database Migration

### Create Migration

```bash
cd phase-3-ai-todo-chatbot/backend

# Generate migration for Conversation and Message tables
uv run alembic revision --autogenerate -m "Add conversation and message tables for AI chatbot"

# Review the generated migration in alembic/versions/
# Ensure it creates conversations and messages tables with proper indexes
```

### Apply Migration

```bash
# Apply migration to database
uv run alembic upgrade head

# Verify tables created
uv run python -c "from src.db.session import engine; from sqlmodel import text; with engine.connect() as conn: print(conn.execute(text('SELECT tablename FROM pg_tables WHERE schemaname = \\\'public\\\'')).fetchall())"
```

**Expected Tables**:
- `conversations` - Chat threads
- `messages` - Chat messages
- Existing Phase II tables (tasks, tags, task_tags, users, sessions, accounts)

---

## Step 4: Start Development Servers

### Terminal 1: Backend Server

```bash
cd phase-3-ai-todo-chatbot/backend

# Start FastAPI server with auto-reload
uv run uvicorn src.main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Verify Backend**:
- Open http://localhost:8000/docs
- Check `/api/health` endpoint returns 200 OK
- Verify `/api/chatkit` endpoint is listed (requires JWT)

### Terminal 2: Frontend Server

```bash
cd phase-3-ai-todo-chatbot/frontend

# Start Next.js development server
npm run dev

# Expected output:
# ▲ Next.js 16.x.x
# - Local:        http://localhost:3000
# - Ready in X.Xs
```

**Verify Frontend**:
- Open http://localhost:3000
- Login with existing Phase II credentials
- Navigate to dashboard
- Verify GlobalChatButton appears (floating button)

---

## Step 5: Test ChatKit Integration

### Manual Testing

1. **Open Dashboard**: Navigate to http://localhost:3000/dashboard
2. **Click Chat Button**: Click the floating chat button (bottom-right corner)
3. **Send Test Message**: Type "Add a task to buy groceries"
4. **Verify Response**: Agent should respond with confirmation
5. **Check Task Created**: Verify task appears in task list

### Test Commands

**Add Task**:
```
Add a task to buy groceries
Add an urgent task to fix the bug
Create a task to call mom tomorrow
```

**List Tasks**:
```
Show me my tasks
What's pending?
Show high priority tasks
What's due today?
```

**Complete Task**:
```
Mark task 1 as complete
I finished buying groceries
Complete the grocery task
```

**Delete Task**:
```
Delete task 2
Remove the meeting task
```

**Update Task**:
```
Change task 1 to high priority
Rename the grocery task to "Buy groceries and fruits"
```

### Expected Behavior

- ✅ Responses stream progressively (not all at once)
- ✅ Agent understands natural language variations
- ✅ Tasks created/updated/deleted correctly
- ✅ User can only see their own tasks
- ✅ Conversation history persists across page refreshes

---

## Step 6: Verify MCP Tools

### Test MCP Server Directly

```bash
cd phase-3-ai-todo-chatbot/backend

# Test MCP server in isolation
uv run python -c "
from mcp_server.tools import add_task, list_tasks
import asyncio

async def test():
    # Test add_task
    result = add_task(user_id='test-user', title='Test Task', priority='high')
    print('Add Task Result:', result)

    # Test list_tasks
    result = list_tasks(user_id='test-user', status='all')
    print('List Tasks Result:', result)

asyncio.run(test())
"
```

### Verify Tool Registration

```bash
# Check MCP tools are registered
uv run python -c "
from mcp_server.tools import mcp
print('Registered Tools:', [tool.name for tool in mcp._tools])
"

# Expected output:
# Registered Tools: ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task', 'set_priority', 'get_task']
```

---

## Step 7: Run Tests

### Backend Tests

```bash
cd phase-3-ai-todo-chatbot/backend

# Run all tests
uv run pytest

# Run specific test suites
uv run pytest tests/unit/test_mcp_tools.py -v
uv run pytest tests/unit/test_chatkit_store.py -v
uv run pytest tests/integration/test_chatkit_endpoint.py -v

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

**Expected Results**:
- All tests pass
- Coverage > 80%
- No user isolation violations

### Frontend Tests

```bash
cd phase-3-ai-todo-chatbot/frontend

# Run component tests
npm test

# Run specific test
npm test -- chatkit-widget.test.tsx
```

---

## Step 8: Troubleshooting

### Common Issues

**Issue: "OPENAI_API_KEY environment variable is required"**
- **Solution**: Set `OPENAI_API_KEY` in backend `.env` file
- **Alternative**: Switch to free provider (OpenRouter) with `LLM_PROVIDER=openrouter`

**Issue: "Failed to connect to database"**
- **Solution**: Verify `DATABASE_URL` is correct in `.env`
- **Check**: Neon database is running and accessible
- **Test**: `psql $DATABASE_URL -c "SELECT 1"`

**Issue: "JWT token invalid"**
- **Solution**: Ensure `BETTER_AUTH_SECRET` matches in both frontend and backend
- **Verify**: Both `.env` files have identical secret
- **Regenerate**: `openssl rand -base64 32`

**Issue: "ChatKit widget shows blank screen"**
- **Solution**: Check browser console for errors
- **Verify**: `NEXT_PUBLIC_CHATKIT_URL` is correct
- **Test**: `curl http://localhost:8000/api/chatkit` (should return 401 without JWT)

**Issue: "Agent responses are slow"**
- **Solution**: Switch to faster provider (Groq) with `LLM_PROVIDER=groq`
- **Alternative**: Use smaller model (gpt-4o-mini instead of gpt-4o)
- **Check**: Network latency to LLM provider

**Issue: "User can see other users' tasks"**
- **CRITICAL**: This is a security violation
- **Check**: JWT validation in `/api/chatkit` endpoint
- **Verify**: All MCP tools validate `user_id`
- **Test**: Run user isolation tests

### Debug Mode

Enable debug logging:

```bash
# Backend
export LOG_LEVEL=DEBUG
uv run uvicorn src.main:app --reload --port 8000

# Frontend
export NEXT_PUBLIC_DEBUG=true
npm run dev
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/api/health

# Database connection
curl http://localhost:8000/api/health/db

# ChatKit endpoint (requires JWT)
curl -H "Authorization: Bearer $JWT_TOKEN" http://localhost:8000/api/chatkit
```

---

## Step 9: Development Workflow

### Making Changes

1. **Backend Changes**:
   - Edit files in `backend/src/`
   - Server auto-reloads (uvicorn --reload)
   - Test changes with `uv run pytest`

2. **Frontend Changes**:
   - Edit files in `frontend/components/` or `frontend/app/`
   - Browser auto-refreshes (Next.js Fast Refresh)
   - Test changes with `npm test`

3. **Database Changes**:
   - Edit models in `backend/src/models/`
   - Generate migration: `uv run alembic revision --autogenerate -m "description"`
   - Apply migration: `uv run alembic upgrade head`

### Code Quality

```bash
# Backend linting
cd backend
uv run ruff check src/
uv run mypy src/

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

### Git Workflow

```bash
# Create feature branch
git checkout -b 004-ai-chatbot

# Commit changes
git add .
git commit -m "feat: add AI chatbot with ChatKit integration"

# Push to remote
git push origin 004-ai-chatbot

# Create pull request (via GitHub UI)
```

---

## Step 10: Production Deployment

### Environment Variables (Production)

**Backend**:
- Use production `DATABASE_URL` (Neon production database)
- Use production `BETTER_AUTH_SECRET` (different from dev)
- Set `LLM_PROVIDER` to reliable provider (openai recommended)
- Use production API keys (not dev/test keys)
- Set `CORS_ORIGINS` to production frontend URL

**Frontend**:
- Use production `DATABASE_URL` (same as backend)
- Use production `BETTER_AUTH_SECRET` (same as backend)
- Set `NEXT_PUBLIC_API_URL` to production backend URL
- Set `NEXT_PUBLIC_CHATKIT_URL` to production ChatKit endpoint

### Docker Deployment

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .

# Run with docker-compose
docker-compose up -d
```

### Database Migration (Production)

```bash
# Run migrations on production database
uv run alembic upgrade head

# Verify tables created
uv run python -c "from src.db.session import engine; from sqlmodel import text; with engine.connect() as conn: print(conn.execute(text('SELECT COUNT(*) FROM conversations')).scalar())"
```

---

## Summary

You should now have:
- ✅ Backend running with ChatKit endpoint
- ✅ Frontend with ChatKit widget
- ✅ Database with Conversation and Message tables
- ✅ MCP tools for task operations
- ✅ Multi-provider LLM support
- ✅ JWT authentication and user isolation
- ✅ Tests passing

**Next Steps**:
1. Implement additional features (Phase IV)
2. Optimize performance (caching, connection pooling)
3. Add monitoring and logging
4. Deploy to production

**Support**:
- Documentation: `specs/004-ai-chatbot/`
- Reference Code: `reference-code/`
- Issues: Create GitHub issue with logs and error messages
