# Implementation Plan: AI-Powered Conversational Task Management

**Branch**: `004-ai-chatbot` | **Date**: 2026-01-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature enables users to manage their todo tasks through natural language conversation instead of traditional UI interactions. Users can say "Add a task to buy groceries" or "Show me what's due today" and the system understands and responds helpfully. The implementation uses OpenAI Agents SDK with multi-provider LLM support (OpenAI, Gemini, Groq, OpenRouter), FastMCP for tool orchestration, and ChatKit protocol for the conversational interface. All conversation history persists in the database with stateless architecture - no in-memory sessions. User isolation is strictly enforced via JWT authentication with user_id validation in all MCP tools.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Agents SDK (openai-agents>=0.2.9), FastMCP (mcp>=1.0.0), openai-chatkit-python (chatkit>=0.1.0), sse-starlette, asyncpg, python-jose
- Frontend: Next.js 16 (App Router), openai-chatkit-react, Better Auth, Tailwind CSS, Shadcn UI
**Storage**: Neon Serverless PostgreSQL (asyncpg driver) - Conversation and Message tables for chat persistence, existing Task tables for task operations
**Testing**: pytest (backend unit/integration tests), Jest/React Testing Library (frontend component tests)
**Target Platform**: Linux server (Docker containers), Web browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application (full-stack) - Backend API + Frontend SPA
**Performance Goals**:
- Response streaming starts within 1 second of user message
- Support 100 concurrent conversations without degradation
- 95%+ accuracy in natural language command interpretation
**Constraints**:
- Stateless architecture - no in-memory session state
- All conversation history fetched from database on every request
- JWT authentication required for all endpoints
- User isolation enforced - zero cross-user data access
- 2-day message retention policy for database storage optimization
**Scale/Scope**:
- Support 100+ concurrent users
- Handle conversations with 50+ messages
- 7 MCP tools for task operations (add, list, complete, delete, update, set_priority, get_task)
- Multi-provider LLM support (4 providers: OpenAI, Gemini, Groq, OpenRouter)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase III Mandatory Requirements Compliance

✅ **Tech Stack**: Uses OpenAI Agents SDK (openai-agents>=0.2.9), Official MCP Python SDK (FastMCP from mcp>=1.0.0), openai-chatkit-python (backend), and openai-chatkit-react (frontend). No alternative frameworks.

✅ **Conversational Interface**: Primary method for AI-powered task management. Users manage tasks through natural language conversation via ChatKit widget.

✅ **Natural Language Task Management**: All 5 Basic Level features (Add, List, Complete, Delete, Update) work via natural language commands through MCP tools.

✅ **Stateless Architecture**: Chat endpoints completely stateless. All conversation history fetched from database (Conversation/Message tables) on every request. No in-memory session state. Agent uses SQLiteSession for temporary conversation context during request processing only.

✅ **Conversation Persistence & Context**: All conversations and messages persist in Neon database tables. Uses openai-chatkit-python Store contracts (DatabaseStore for production, MemoryStore for testing) to maintain context across multiple messages and sessions.

✅ **Secure MCP Tools**: All 7 MCP tools are stateless, single-purpose, and reuse existing backend TaskService. Every tool validates user_id matches authenticated user from JWT. Tools do NOT bypass user isolation.

✅ **Error Handling & Feedback**: Chatbot provides helpful error messages when commands are not understood. Confirms all successful task operations with friendly, deterministic responses. No silent failures or ambiguous confirmations.

✅ **Reliability**: All MCP tools have unit tests with mock agent. Integration tests for ChatKit endpoint with JWT authentication. User isolation tests verify security. Deterministic response tests ensure reliability.

### Quality & Verification Gates

✅ **Type Safety Enforcement**: Backend uses Python 3.13+ with type hints. Frontend uses TypeScript with strict mode.

✅ **Explicit Error Handling**: All MCP tools return structured error responses. ChatKit server handles exceptions gracefully with user-friendly messages.

✅ **12-Factor Alignment**: Configuration via environment variables (LLM_PROVIDER, API keys, DATABASE_URL). Stateless processes. Logs to stdout/stderr.

✅ **Code Quality**: No placeholder logic. All code follows existing patterns from Phase II. Reuses TaskService for task operations.

✅ **Automated Testing**: Backend includes unit tests for MCP tools and integration tests for ChatKit endpoint. Tests verify JWT authentication and user isolation.

### Specification-First Discipline

✅ **Specification Exists**: Feature specification at `specs/004-ai-chatbot/spec.md` defines all requirements, user stories, and success criteria.

✅ **Implementation Plan**: This plan document defines technical approach, architecture, and implementation details before coding begins.

**GATE STATUS**: ✅ PASSED - All constitutional requirements satisfied. Ready to proceed with Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/004-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── chatkit-endpoint.yaml  # OpenAPI spec for /api/chatkit
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (phase-3-ai-todo-chatbot/)

```text
phase-3-ai-todo-chatbot/
├── backend/                     # FastAPI Backend (Phase 2 + Phase 3)
│   ├── src/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── chatkit.py   # NEW: ChatKit endpoint
│   │   ├── auth/                # Existing: JWT validation
│   │   ├── db/
│   │   │   ├── session.py       # Existing: Sync sessions
│   │   │   └── async_session.py # NEW: Async sessions for ChatKit
│   │   ├── models/
│   │   │   ├── task.py          # Existing: Task model
│   │   │   ├── conversation.py  # NEW: Conversation model
│   │   │   └── message.py       # NEW: Message model
│   │   ├── services/
│   │   │   ├── task_service.py  # Existing: Task CRUD
│   │   │   ├── chatkit_server.py # NEW: TaskChatKitServer
│   │   │   └── chatkit_store.py  # NEW: DatabaseStore, MemoryStore
│   │   ├── agent_config/
│   │   │   ├── __init__.py      # NEW: TodoAgent class
│   │   │   └── factory.py       # NEW: Multi-provider LLM factory
│   │   └── main.py              # Updated: Register chatkit router
│   ├── mcp_server/
│   │   └── tools.py             # NEW: 7 MCP tools with FastMCP
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_mcp_tools.py # NEW: MCP tool unit tests
│   │   │   └── test_chatkit_store.py # NEW: Store tests
│   │   └── integration/
│   │       └── test_chatkit_endpoint.py # NEW: ChatKit integration tests
│   ├── alembic/
│   │   └── versions/
│   │       └── xxx_add_conversation_message.py # NEW: Migration
│   ├── pyproject.toml           # Updated: Add Phase 3 dependencies
│   └── .env.example             # Updated: Add LLM provider vars
│
└── frontend/                    # Next.js 16 Frontend (Phase 2 + Phase 3)
    ├── app/
    │   └── dashboard/
    │       └── page.tsx         # Updated: Add GlobalChatButton
    ├── components/
    │   └── chat/
    │       ├── chatkit-widget.tsx # NEW: ChatKit React widget
    │       └── global-chat-button.tsx # NEW: Floating chat button
    ├── lib/
    │   └── auth.ts              # Existing: Better Auth client
    ├── package.json             # Updated: Add openai-chatkit-react
    └── .env.example             # Updated: Add NEXT_PUBLIC_CHATKIT_URL
```

**Structure Decision**: Web application (full-stack) with separate backend and frontend directories. Phase 3 builds on top of existing Phase 2 code in `phase-3-ai-todo-chatbot/` directory. Backend adds AI chatbot capabilities (ChatKit server, MCP tools, agent configuration, conversation persistence). Frontend adds ChatKit widget and global chat button. All new code follows existing Phase 2 patterns and conventions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
