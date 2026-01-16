---
id: 0002
title: Create AI Chatbot Implementation Plan
stage: plan
date: 2026-01-12
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-ai-chatbot
branch: 004-ai-chatbot
user: sunaina_ubuntu
command: /sp.plan
labels: ["planning", "ai-chatbot", "chatkit", "openai-agents", "mcp", "phase-3"]
links:
  spec: specs/004-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-ai-chatbot/plan.md
  - specs/004-ai-chatbot/research.md
  - specs/004-ai-chatbot/data-model.md
  - specs/004-ai-chatbot/contracts/chatkit-endpoint.md
  - specs/004-ai-chatbot/quickstart.md
  - CLAUDE.md (updated)
tests:
  - None (planning phase - no tests written yet)
---

## Prompt

```
/sp.plan Use Context7 MCP to research the latest documentation for OpenAI Agents SDK, FastMCP, openai-chatkit-python, and openai-chatkit-react. Read the reference-code directory to understand the existing implementation patterns.

The AI chatbot feature uses the following mandatory tech stack (as per constitution Phase III requirements):

**Backend Architecture:**
- OpenAI Agents SDK with multi-provider LLM support (OpenAI, Gemini, Groq, OpenRouter via OpenAI-compatible endpoints)
- FastMCP from Official MCP Python SDK (mcp package) for tool orchestration
- openai-chatkit-python for ChatKit server implementation with Store contracts
- FastAPI for /api/chatkit endpoint with Better Auth JWT authentication
- SQLModel for Conversation and Message database models
- Neon PostgreSQL for conversation persistence
- SSE (Server-Sent Events) via sse-starlette for streaming responses

**MCP Tools (7 stateless tools):**
- add_task, list_tasks, complete_task, delete_task, update_task, set_priority, get_task
- Each tool MUST validate user_id matches authenticated user for security
- Tools MUST reuse existing backend services (no direct database access)
- Tools MUST be single-purpose and deterministic

**Agent Configuration:**
- TodoAgent with SQLiteSession for conversation memory
- Multi-provider LLM factory pattern supporting provider switching
- System prompt for natural language task management
- Context maintenance across conversation turns

**Store Implementations:**
- DatabaseStore for production (persists to Neon PostgreSQL Conversation/Message tables)
- MemoryStore for testing (in-memory conversation history)

**Frontend Architecture:**
- openai-chatkit-react for ChatKit widget component
- Better Auth JWT token passed to ChatKit for authentication
- GlobalChatButton floating component for easy access
- Integration with existing Next.js 16 App Router structure

**Stateless Architecture Requirements:**
- NO in-memory session state on backend
- ALL conversation history fetched from database on every request
- Agent uses SQLiteSession for temporary conversation context during request processing
- Store contracts handle persistence to database

**Security & User Isolation:**
- JWT authentication on /api/chatkit endpoint
- user_id extracted from JWT and passed to all MCP tools
- Every MCP tool MUST validate user_id matches authenticated user
- Zero cross-user data access

**Natural Language Processing:**
- Priority keyword detection (urgent, important, high, low, medium)
- Flexible task references (by ID or by title/description)
- Context-aware responses using conversation history
- Friendly confirmations and helpful error messages

**Testing Strategy:**
- Unit tests for all MCP tools with mock agent
- Integration tests for ChatKit endpoint with JWT authentication
- User isolation tests to verify security
- Deterministic response tests for reliability

Produce: architecture sketch, data model (Conversation, Message tables), API contracts (/api/chatkit endpoint), MCP tool specifications, agent configuration, Store implementations, error taxonomy, and NFRs (95% accuracy, <1s response time, 100 concurrent users). the phase-3 will go in the phase-3-ai-todo-chatbot where i already copied the phase-2 code so continue in this
```

## Response snapshot

Successfully created comprehensive implementation plan for AI-powered conversational task management feature (004-ai-chatbot). The planning workflow included:

**Phase 0 - Research**: Researched OpenAI Agents SDK, FastMCP, ChatKit libraries via Context7 MCP. Read reference-code implementation patterns. Consolidated findings in research.md with technology decisions and rationale for all 7 major components.

**Phase 1 - Design**:
- Filled Technical Context and Constitution Check in plan.md (all gates passed)
- Generated data-model.md with Conversation and Message table schemas, indexes, business rules, and SQLModel definitions
- Generated API contracts in contracts/chatkit-endpoint.md with full ChatKit protocol specification, MCP tool contracts, authentication flow, and error handling
- Generated quickstart.md with 10-step development setup guide including environment configuration, dependency installation, database migration, testing, and troubleshooting

**Phase 1 - Agent Context Update**: Updated CLAUDE.md with Phase 3 technologies (Python 3.13+, TypeScript 5.x, Neon PostgreSQL with Conversation/Message tables)

**Key Architectural Decisions**:
1. OpenAI Agents SDK with multi-provider LLM support (OpenAI, Gemini, Groq, OpenRouter)
2. FastMCP for tool orchestration with 7 stateless MCP tools
3. ChatKit protocol (openai-chatkit-python + openai-chatkit-react) for conversational interface
4. Stateless architecture with database-backed conversation persistence
5. JWT authentication with user_id validation in all MCP tools
6. DatabaseStore (production) and MemoryStore (testing) implementations
7. 2-day message retention policy for storage optimization

**Constitutional Compliance**: All Phase III mandatory requirements satisfied - tech stack, conversational interface, natural language task management, stateless architecture, conversation persistence, secure MCP tools, error handling, and reliability.

## Outcome

- ✅ Impact: Complete implementation plan created with research, data model, API contracts, and quickstart guide. All constitutional requirements validated. Ready for /sp.tasks to break down into actionable implementation tasks.
- 🧪 Tests: No tests written (planning phase). Test strategy documented in research.md and quickstart.md.
- 📁 Files: Created 5 planning artifacts (plan.md, research.md, data-model.md, contracts/chatkit-endpoint.md, quickstart.md). Updated CLAUDE.md with Phase 3 technologies.
- 🔁 Next prompts: /sp.tasks to generate actionable task breakdown, then implementation phase
- 🧠 Reflection: Planning workflow executed successfully with comprehensive research via Context7 and reference code analysis. All artifacts align with SpecKit Plus format and constitutional requirements. Multi-provider LLM support provides flexibility for development (free tier) and production (reliability).

## Evaluation notes (flywheel)

- Failure modes observed: None. Planning workflow completed without errors or blockers.
- Graders run and results (PASS/FAIL): Constitutional compliance check PASSED (all Phase III requirements satisfied). Specification alignment PASSED (all requirements from spec.md addressed in plan).
- Prompt variant (if applicable): Standard /sp.plan workflow with detailed technical requirements
- Next experiment (smallest change to try): Consider adding ADR for multi-provider LLM strategy and Store contract implementation approach as suggested in research.md
