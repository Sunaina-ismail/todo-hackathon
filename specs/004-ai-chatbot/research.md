# Technology Research: AI-Powered Conversational Task Management

**Feature**: 004-ai-chatbot
**Date**: 2026-01-12
**Phase**: Phase 0 - Technology Research

## Overview

This document consolidates research findings for implementing natural language task management through conversational AI. All technology choices align with Phase III constitutional requirements and build upon existing Phase II infrastructure.

---

## 1. OpenAI Agents SDK (openai-agents>=0.2.9)

### Decision
Use OpenAI Agents SDK as the primary framework for building the conversational AI agent.

### Rationale
- **Constitutional Requirement**: Phase III mandates OpenAI Agents SDK - no alternatives permitted
- **Multi-Provider Support**: Native support for OpenAI, plus integration with 100+ LLM providers via OpenAI-compatible endpoints (Gemini, Groq, OpenRouter)
- **Built-in Memory**: SQLiteSession provides persistent conversation context across multiple turns
- **Tool Integration**: Seamless integration with MCP tools via MCPServerStdio transport
- **Streaming Support**: Native streaming responses for progressive text rendering
- **Production Ready**: Official OpenAI SDK with active maintenance and documentation

### Key Features Used
- **Agent**: Core agent class with instructions, model, and tools
- **Runner**: Executes agent with streaming support (`Runner.run_streamed`)
- **SQLiteSession**: File-based conversation memory (user_id + thread_id as session key)
- **OpenAIChatCompletionsModel**: Model wrapper supporting multiple providers via base_url override

### Integration Pattern
```python
from agents import Agent, Runner, SQLiteSession
from agents import OpenAIChatCompletionsModel

# Create agent with tools
agent = Agent(
    name="TodoAgent",
    model=create_model(),  # Multi-provider factory
    instructions="System prompt for task management",
    tools=[mcp_server]  # MCP tools via MCPServerStdio
)

# Run with session for memory
session = SQLiteSession(f"user_{user_id}_thread_{thread_id}", "chat_sessions.db")
result = Runner.run_streamed(agent, user_message, session=session)
```

### Version & Compatibility
- **Version**: openai-agents>=0.2.9
- **Python**: Requires Python 3.10+
- **Dependencies**: openai>=1.0.0, pydantic>=2.0

### Alternatives Considered
- **LangChain**: More complex, heavier framework. Rejected per constitutional mandate.
- **Custom Implementation**: Would require building conversation memory, streaming, tool orchestration from scratch. Not permitted.

---

## 2. FastMCP (Official MCP Python SDK)

### Decision
Use FastMCP from the official MCP Python SDK (mcp>=1.0.0) for tool orchestration.

### Rationale
- **Constitutional Requirement**: Phase III mandates Official MCP Python SDK - no alternatives permitted
- **Pythonic API**: Simple decorator-based tool registration (`@mcp.tool()`)
- **Stdio Transport**: Automatic stdio transport handling for agent integration
- **Type Safety**: Full type hint support with automatic schema generation
- **Zero Configuration**: Works out-of-box with OpenAI Agents SDK via MCPServerStdio

### Key Features Used
- **FastMCP**: Main server class for tool registration
- **@mcp.tool()**: Decorator for registering Python functions as MCP tools
- **Stdio Transport**: Default transport for local agent-tool communication
- **Automatic Schema**: Generates tool schemas from Python type hints

### Integration Pattern
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="todo-task-server")

@mcp.tool()
def add_task(user_id: str, title: str, description: Optional[str] = None) -> dict:
    """Create a new task for a user."""
    # Implementation using TaskService
    return {"task_id": "...", "status": "created"}

# Agent connects via MCPServerStdio
from agents.extensions.mcp import MCPServerStdio
mcp_server = MCPServerStdio("python", ["mcp_server/tools.py"])
```

### Tool Design Principles
1. **Stateless**: No in-memory state - all data from database
2. **Single-Purpose**: Each tool does one thing well
3. **User Isolation**: Every tool validates user_id matches authenticated user
4. **Service Reuse**: Tools call existing TaskService methods (no direct DB access)
5. **Deterministic**: Same input always produces same output

### Version & Compatibility
- **Version**: mcp>=1.0.0 (FastMCP included)
- **Python**: Requires Python 3.10+
- **Transport**: Stdio (default), SSE, WebSocket supported

### Alternatives Considered
- **Direct Function Tools**: OpenAI Agents SDK supports direct function tools, but MCP provides better separation of concerns and testability.
- **Custom Tool Protocol**: Would require implementing tool discovery, schema generation, and transport. Not permitted.

---

## 3. ChatKit Protocol (openai-chatkit-python + openai-chatkit-react)

### Decision
Use official ChatKit libraries for conversational interface:
- **Backend**: openai-chatkit-python (chatkit>=0.1.0)
- **Frontend**: openai-chatkit-react

### Rationale
- **Constitutional Requirement**: Phase III mandates ChatKit - no alternative chat implementations permitted
- **Protocol Compliance**: Official ChatKit protocol for threads, messages, widgets
- **Store Contracts**: Built-in Store interface for conversation persistence (DatabaseStore, MemoryStore)
- **Streaming Support**: Native SSE streaming for progressive text rendering
- **Widget Support**: Structured UI widgets for rich responses
- **Frontend Integration**: React components with authentication and theming

### Backend: openai-chatkit-python

**Key Features Used**:
- **ChatKitServer**: Base server class for handling ChatKit protocol requests
- **Store Interface**: Abstract interface for conversation persistence
  - `DatabaseStore`: Production implementation with Neon PostgreSQL
  - `MemoryStore`: Testing implementation with in-memory storage
- **ThreadMetadata**: Thread information (id, title, created_at, updated_at)
- **StreamingResult**: SSE streaming response wrapper
- **AgentContext**: Context object passed to agent with thread, store, request_context

**Integration Pattern**:
```python
from chatkit.server import ChatKitServer, Store
from chatkit.agents import AgentContext, stream_agent_response

class TaskChatKitServer(ChatKitServer):
    def __init__(self, store: Store):
        super().__init__(store)
        self.agent = TodoAgent().get_agent()

    async def respond(self, thread, input, context):
        agent_context = AgentContext(thread=thread, store=self.store, request_context=context)
        session = SQLiteSession(f"user_{context['user_id']}_thread_{thread.id}", "chat_sessions.db")

        result = Runner.run_streamed(self.agent, input, session=session, context=agent_context)
        async for event in stream_agent_response(agent_context, result):
            yield event
```

### Frontend: openai-chatkit-react

**Key Features Used**:
- **useChatKit**: React hook for ChatKit control and configuration
- **ChatKit**: Main widget component for chat interface
- **getClientSecret**: Authentication callback for JWT token management
- **Custom Fetch**: Override fetch for adding Authorization headers

**Integration Pattern**:
```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';

const { control } = useChatKit({
  api: {
    url: process.env.NEXT_PUBLIC_CHATKIT_URL,
    async getClientSecret() {
      // Return JWT token from Better Auth
      const session = await auth.api.getSession();
      return session.token;
    },
    fetch: (url, options) => {
      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${token}`,
        },
      });
    },
  },
});

return <ChatKit control={control} className="h-[600px] w-[400px]" />;
```

### Store Implementation Strategy

**DatabaseStore (Production)**:
- Persists threads and messages to Neon PostgreSQL
- Uses async SQLModel sessions
- Implements full Store interface (create_thread, add_message, get_thread, list_threads, etc.)
- Enforces user isolation via user_id filtering

**MemoryStore (Testing)**:
- In-memory dictionary storage
- Fast for unit tests
- No database dependencies
- Same interface as DatabaseStore

### Version & Compatibility
- **Backend**: chatkit>=0.1.0 (openai-chatkit-python)
- **Frontend**: @openai/chatkit-react (latest)
- **Python**: Requires Python 3.10+
- **React**: Requires React 18+

### Alternatives Considered
- **Custom SSE Streaming**: Reference code includes custom SSE implementation, but official ChatKit provides superior protocol compliance and widget support. Custom implementation disabled per user requirement.

---

## 4. Multi-Provider LLM Support

### Decision
Implement multi-provider LLM factory supporting OpenAI, Gemini, Groq, and OpenRouter.

### Rationale
- **Flexibility**: Users can switch providers via environment variable
- **Cost Optimization**: Different providers have different pricing (OpenRouter has free tier)
- **Reliability**: Fallback options if primary provider has issues
- **Development**: Free/cheap options for development (OpenRouter free models, Groq)

### Provider Configuration

**OpenAI (Default)**:
- **Endpoint**: https://api.openai.com/v1
- **Models**: gpt-4o, gpt-4o-mini, gpt-4-turbo
- **Pros**: Most reliable, best documentation, highest quality
- **Cons**: Paid API, higher cost than alternatives
- **Use Case**: Production deployments requiring reliability

**Gemini (Google)**:
- **Endpoint**: https://generativelanguage.googleapis.com/v1beta/openai/
- **Models**: gemini-2.5-flash, gemini-2.5-pro
- **Pros**: Competitive pricing, good quality, multi-modal support
- **Cons**: Requires Google API key, less documentation
- **Use Case**: Cost optimization, multi-modal tasks

**Groq (Fast Inference)**:
- **Endpoint**: https://api.groq.com/openai/v1
- **Models**: llama-3.3-70b-versatile, mixtral-8x7b
- **Pros**: Extremely fast inference, free tier available
- **Cons**: Limited model selection, newer service
- **Use Case**: Development, speed-critical applications

**OpenRouter (Multi-Model Proxy)**:
- **Endpoint**: https://openrouter.ai/api/v1
- **Models**: openai/gpt-oss-20b:free, google/gemma-2-9b-it:free, and 100+ others
- **Pros**: Access to multiple providers, some free models, unified API
- **Cons**: Proxy adds latency, free models have rate limits
- **Use Case**: Development (free tier), multi-model experimentation

### Implementation Pattern
```python
def create_model(provider: str | None = None, model: str | None = None):
    provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()

    if provider == "gemini":
        client = AsyncOpenAI(api_key=os.getenv("GEMINI_API_KEY"),
                            base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        model_name = model or os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")
    elif provider == "groq":
        client = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"),
                            base_url="https://api.groq.com/openai/v1")
        model_name = model or os.getenv("GROQ_DEFAULT_MODEL", "llama-3.3-70b-versatile")
    # ... other providers

    return OpenAIChatCompletionsModel(model=model_name, openai_client=client)
```

### Environment Variables
```bash
# Provider selection
LLM_PROVIDER=openai  # openai | gemini | groq | openrouter

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# Gemini
GEMINI_API_KEY=AIza...
GEMINI_DEFAULT_MODEL=gemini-2.5-flash

# Groq
GROQ_API_KEY=gsk_...
GROQ_DEFAULT_MODEL=llama-3.3-70b-versatile

# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_DEFAULT_MODEL=openai/gpt-oss-20b:free
```

---

## 5. Database Schema (Conversation Persistence)

### Decision
Add Conversation and Message tables to existing Neon PostgreSQL database using SQLModel.

### Rationale
- **Stateless Architecture**: No in-memory sessions - all state in database
- **User Isolation**: Conversation and Message tables include user_id for filtering
- **ChatKit Integration**: Schema aligns with ChatKit Store interface requirements
- **Existing Infrastructure**: Reuses Phase II database connection and migration system

### Schema Design

**Conversation Table**:
- `id` (UUID, PK): Unique conversation identifier
- `user_id` (String, indexed): Owner of conversation
- `thread_id` (String, unique, indexed): ChatKit thread ID
- `title` (String): Conversation title (auto-generated or user-set)
- `is_active` (Boolean, indexed): Active status for archiving
- `created_at` (DateTime, indexed): Creation timestamp
- `updated_at` (DateTime, indexed): Last message timestamp

**Message Table**:
- `id` (UUID, PK): Unique message identifier
- `conversation_id` (UUID, FK): Parent conversation
- `user_id` (String, indexed): Message owner (for isolation)
- `role` (String): Message role (user, assistant, system)
- `content` (Text): Message content
- `created_at` (DateTime, indexed): Message timestamp

### Indexes
- `conversations.user_id`: Fast user conversation lookup
- `conversations.thread_id`: Fast thread lookup for ChatKit
- `conversations.(user_id, created_at DESC)`: Optimized sorted queries
- `messages.conversation_id`: Fast message retrieval
- `messages.(conversation_id, created_at)`: Ordered message queries
- `messages.user_id`: User isolation enforcement

### Retention Policy
- Messages older than 2 days automatically deleted (background task)
- Conversations without messages for 30 days archived (is_active=false)
- Archived conversations deleted after 90 days

---

## 6. Authentication & Security

### Decision
Reuse existing Better Auth JWT authentication with user_id validation in all MCP tools.

### Rationale
- **Existing Infrastructure**: Phase II already implements JWT authentication
- **User Isolation**: JWT contains user_id - passed to all MCP tools for validation
- **Stateless**: No session state - JWT verified on every request
- **ChatKit Integration**: JWT token passed via Authorization header to /api/chatkit endpoint

### Security Flow
1. Frontend: Better Auth generates JWT token on login
2. Frontend: Passes JWT in Authorization header to /api/chatkit
3. Backend: Verifies JWT signature using BETTER_AUTH_SECRET
4. Backend: Extracts user_id from JWT payload
5. Backend: Passes user_id to ChatKit server in context
6. ChatKit Server: Passes user_id to all MCP tools
7. MCP Tools: Validate user_id matches authenticated user before operations

### User Isolation Enforcement
Every MCP tool MUST:
```python
@mcp.tool()
def add_task(user_id: str, title: str) -> dict:
    # user_id comes from JWT (authenticated user)
    # Tool validates user_id before any database operations
    # TaskService.create_task enforces user_id filtering
    return TaskService.create_task(session, user_id, task_data)
```

---

## 7. Testing Strategy

### Decision
Implement comprehensive testing at multiple levels: unit tests for MCP tools, integration tests for ChatKit endpoint, and user isolation tests.

### Test Levels

**Unit Tests (MCP Tools)**:
- Mock TaskService to test tool logic in isolation
- Verify tool input validation and error handling
- Test priority detection and natural language parsing
- Verify deterministic responses

**Integration Tests (ChatKit Endpoint)**:
- Test full request/response cycle with real database
- Verify JWT authentication and user isolation
- Test streaming responses and SSE format
- Verify conversation persistence

**User Isolation Tests**:
- Verify users cannot access other users' tasks
- Verify users cannot access other users' conversations
- Test JWT validation and authorization

### Testing Tools
- **pytest**: Python test framework
- **pytest-asyncio**: Async test support
- **httpx**: HTTP client for API testing
- **SQLModel**: In-memory SQLite for test database

---

## Summary of Technology Decisions

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| AI Agent Framework | OpenAI Agents SDK | >=0.2.9 | Constitutional requirement, multi-provider support, built-in memory |
| Tool Orchestration | FastMCP (Official MCP SDK) | >=1.0.0 | Constitutional requirement, Pythonic API, stdio transport |
| Chat Protocol | openai-chatkit-python | >=0.1.0 | Constitutional requirement, Store contracts, streaming support |
| Frontend Chat | openai-chatkit-react | latest | Official React components, authentication, theming |
| LLM Providers | OpenAI, Gemini, Groq, OpenRouter | varies | Flexibility, cost optimization, reliability |
| Database | Neon PostgreSQL (existing) | - | Stateless architecture, conversation persistence |
| Authentication | Better Auth JWT (existing) | - | User isolation, stateless, existing infrastructure |
| Testing | pytest, httpx | latest | Comprehensive coverage, async support |

All technology choices align with Phase III constitutional requirements and build upon existing Phase II infrastructure.
