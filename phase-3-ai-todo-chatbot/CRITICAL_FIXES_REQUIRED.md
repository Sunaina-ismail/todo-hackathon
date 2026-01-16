# 🚨 CRITICAL FIXES REQUIRED - Phase 3 AI Chatbot

**Status**: Implementation has 3 critical issues that MUST be fixed before testing
**Priority**: P0 - Blocking deployment
**Estimated Fix Time**: 3-4 hours

---

## ⚠️ Issues Found

### 1. ChatKit Endpoint - WRONG IMPLEMENTATION ❌

**Current**: Custom REST API with `/threads`, `/messages` endpoints
**Required**: Official ChatKit protocol endpoint at `/api/chatkit`

**Impact**: Frontend ChatKit widget cannot communicate with backend
**Fix Location**: `backend/src/api/v1/chatkit.py`
**Reference**: `reference-code/backend/src/api/v1/chatkit.py`

### 2. TodoAgent Configuration - MISSING CRITICAL SETUP ❌

**Current**: Simple MCPServerStdio without proper configuration
**Required**: Full configuration with venv paths, PYTHONPATH, cwd

**Impact**: MCP server will fail to start in WSL/production environments
**Fix Location**: `backend/src/agent_config/__init__.py`
**Reference**: `reference-code/backend/src/agent_config/todo_agent.py`

### 3. Environment Variables - INCOMPLETE ❌

**Current**: Missing all Phase 3 AI configuration
**Required**: LLM provider, API keys, MCP server name

**Impact**: Backend cannot initialize AI agent
**Fix Location**: `backend/.env` and `frontend/.env.local`
**Status**: ✅ FIXED (environment files updated)

---

## ✅ What's Working

- MCP Tools implementation (7 tools with proper user isolation)
- Agent instructions (comprehensive system prompt)
- Multi-provider LLM factory (OpenAI, Gemini, Groq, OpenRouter)
- Database models (Conversation, Message)
- ChatKit stores (DatabaseStore, MemoryStore)

---

## 🔧 Required Actions

### Action 1: Fix ChatKit Endpoint (2 hours)

**File**: `backend/src/api/v1/chatkit.py`

Replace entire file with official ChatKit protocol implementation:

```python
"""ChatKit API Endpoint - Official Protocol Implementation"""

import logging
from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response, StreamingResponse, JSONResponse
from chatkit.server import StreamingResult

from ...auth.dependencies import get_current_user_id
from ...services.chatkit_server import TaskChatKitServer
from ...services.chatkit_store import MemoryStore

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chatkit"])

# ChatKit server will be initialized on first request
_chatkit_server = None

def get_current_user_info(user_id: str = Depends(get_current_user_id)) -> dict:
    """Extract user information from JWT token for ChatKit context."""
    return {
        "id": user_id,
        "name": "there",  # Could be enhanced to get actual user name
    }

async def _get_chatkit_server():
    """Get or create the global ChatKit server instance."""
    global _chatkit_server

    if _chatkit_server is None:
        import os
        use_memory_store = os.environ.get("USE_MEMORY_STORE", "0") == "1"

        if use_memory_store:
            logger.info("Using MemoryStore (USE_MEMORY_STORE=1)")
            from ...services.chatkit_store import MemoryStore
            store = MemoryStore()
        else:
            try:
                from ...db.async_session import get_session_factory
                factory = await get_session_factory()
                if factory is None:
                    logger.warning("Session factory is None, using in-memory store")
                    from ...services.chatkit_store import MemoryStore
                    store = MemoryStore()
                else:
                    from ...services.chatkit_store import DatabaseStore
                    store = DatabaseStore(factory)
                    logger.info("Initialized ChatKit server with DatabaseStore")
            except Exception as e:
                logger.warning(f"Failed to initialize DatabaseStore: {e}, falling back to MemoryStore")
                from ...services.chatkit_store import MemoryStore
                store = MemoryStore()

        _chatkit_server = TaskChatKitServer(store)

    return _chatkit_server

@router.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    user_info: dict = Depends(get_current_user_info),
) -> Response:
    """
    ChatKit endpoint that processes all chat requests.

    This endpoint:
    1. Authenticates the user via JWT
    2. Extracts the request payload
    3. Processes it through the ChatKit server
    4. Returns streaming (SSE) or JSON response
    """
    user_id = user_info["id"]
    user_name = user_info.get("name", "there")
    logger.info(f"ChatKit request from authenticated user {user_id}")

    try:
        # Read request body
        payload = await request.body()
        logger.info(f"Received payload: {len(payload)} bytes")

        # Add user info to context for the ChatKit server
        context = {
            "user_id": user_id,
            "user_name": user_name,
        }

        # Get or create ChatKit server
        chatkit_server = await _get_chatkit_server()

        # Process through ChatKit server
        result = await chatkit_server.process(payload, context)

        # Return appropriate response type
        if isinstance(result, StreamingResult):
            logger.info(f"Returning streaming response for user {user_id}")
            return StreamingResponse(
                result,
                media_type="text/event-stream",
            )

        # JSON response
        logger.info(f"Returning JSON response for user {user_id}")
        return Response(
            content=result.json,
            media_type="application/json",
        )

    except Exception as e:
        logger.error(f"ChatKit error for user {user_id}: {e}", exc_info=True)
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=500,
        )
```

**Then update** `backend/src/main.py`:
```python
# Replace:
# app.include_router(chatkit_router, prefix="/api")

# With:
app.include_router(chatkit_router)  # No prefix, router already has /api/chatkit
```

---

### Action 2: Fix TodoAgent Configuration (1 hour)

**File**: `backend/src/agent_config/__init__.py`

Replace the `__init__` method:

```python
import os
from pathlib import Path
from agents import Agent
from agents.mcp import MCPServerStdio
from agents.model_settings import ModelSettings

from src.agent_config.factory import create_model

class TodoAgent:
    # ... (keep SYSTEM_INSTRUCTIONS as is)

    def __init__(self, provider: str | None = None, model: str | None = None):
        """Initialize TodoAgent with specified LLM provider and model."""
        # Create LLM model with multi-provider support
        llm_model = create_model(provider=provider, model=model)

        # Get backend directory path
        backend_dir = Path(__file__).parent.parent.parent  # src/agent_config -> src -> backend
        src_dir = backend_dir / "src"

        # Create environment with PYTHONPATH set to include src directory
        env = os.environ.copy()
        current_pythonpath = env.get("PYTHONPATH", "")
        if current_pythonpath:
            env["PYTHONPATH"] = f"{src_dir}:{current_pythonpath}"
        else:
            env["PYTHONPATH"] = str(src_dir)

        # Use venv python directly instead of 'uv run python'
        venv_python = backend_dir / ".venv" / "bin" / "python3"

        # Create MCP server connection via stdio
        self.mcp_server = MCPServerStdio(
            name="task-management-server",
            params={
                "command": str(venv_python),
                "args": ["-m", "mcp_server"],
                "env": env,
                "cwd": str(backend_dir),
            },
            client_session_timeout_seconds=60.0,  # Increased for Neon cold starts
        )

        # Create agent with MCP server
        self.agent = Agent(
            name="TodoAgent",
            model=llm_model,
            instructions=self.SYSTEM_INSTRUCTIONS,
            mcp_servers=[self.mcp_server],
            model_settings=ModelSettings(
                parallel_tool_calls=False,  # Prevent database bottlenecks
            ),
        )

    def get_agent(self) -> Agent:
        """Get configured agent instance."""
        return self.agent
```

---

### Action 3: Add OpenAI API Key (15 minutes)

**File**: `backend/.env`

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Replace `OPENAI_API_KEY=sk-proj-REPLACE_WITH_YOUR_OPENAI_API_KEY` with your actual key

**Alternative**: Use OpenRouter free tier:
```bash
# In backend/.env, change:
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
OPENROUTER_DEFAULT_MODEL=openai/gpt-oss-20b:free
```

Get free OpenRouter key from: https://openrouter.ai/

---

## 📋 Testing Checklist

After applying all fixes:

```bash
# 1. Start backend
cd phase-3-ai-todo-chatbot/backend
uv run uvicorn src.main:app --reload --port 8001

# Check logs for:
# ✅ "Initialized ChatKit server with DatabaseStore"
# ✅ "task-management-server" MCP connection
# ❌ No errors about missing API keys or MCP failures

# 2. Test ChatKit endpoint
curl -X POST http://localhost:8001/api/chatkit \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"thread.create"}'

# Should return ChatKit protocol response (not 404)

# 3. Start frontend
cd phase-3-ai-todo-chatbot/frontend
npm run dev

# 4. Test in browser
# - Login to dashboard
# - Click floating chat button
# - Send message: "Add a task to buy groceries"
# - Verify: Task created and agent responds
```

---

## 📚 Reference Files

- **Verification Report**: `VERIFICATION_REPORT.md` (detailed analysis)
- **Reference Implementation**: `reference-code/backend/src/api/v1/chatkit.py`
- **Reference Agent**: `reference-code/backend/src/agent_config/todo_agent.py`
- **Specification**: `specs/004-ai-chatbot/spec.md`
- **Tasks**: `specs/004-ai-chatbot/tasks.md`

---

## 🎯 Success Criteria

- [ ] Backend starts without errors
- [ ] MCP server connects successfully
- [ ] ChatKit endpoint responds to protocol requests
- [ ] Agent can execute MCP tools
- [ ] Conversation history persists
- [ ] User isolation enforced
- [ ] Streaming responses work

---

**Created**: 2026-01-15
**Priority**: P0 - CRITICAL
**Estimated Fix Time**: 3-4 hours
**Status**: Awaiting implementation
