# Implementation Tasks: AI-Powered Conversational Task Management

**Feature**: 004-ai-chatbot | **Branch**: `004-ai-chatbot` | **Date**: 2026-01-12

**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Data Model**: [data-model.md](./data-model.md)

---

## Overview

This document breaks down the implementation of the AI-powered conversational task management feature into actionable tasks. Tasks are organized by user story to enable independent implementation and testing. Each phase represents a complete, testable increment.

**Implementation Strategy**: MVP-first approach focusing on P1 user stories (Add, View, Context) before P2/P3 features.

**Subagents Available**:
- `backend-expert`: FastAPI development, SQLModel, database integration
- `auth-expert`: JWT authentication, Better Auth integration
- `chatkit-backend-engineer`: ChatKit server, OpenAI Agents SDK, MCP tools
- `chatkit-frontend-engineer`: ChatKit React widget, frontend integration
- `frontend-expert`: Next.js 16, App Router, React components

**MCP Tools Available**:
- `context7`: Research latest documentation for libraries
- `github`: Repository operations, PR creation

---

## Task Summary

| Phase | User Story | Task Count | Parallelizable |
|-------|-----------|------------|----------------|
| Phase 1 | Setup | 5 | 3 |
| Phase 2 | Foundational | 8 | 5 |
| Phase 3 | US1 (Add Tasks) + US2 (View Tasks) + US6 (Context) | 12 | 7 |
| Phase 4 | US7 (Resume Sessions) | 3 | 2 |
| Phase 5 | US3 (Complete Tasks) | 4 | 3 |
| Phase 6 | US4 (Delete Tasks) + US5 (Update Tasks) | 6 | 5 |
| Phase 7 | Polish & Testing | 6 | 4 |
| **Total** | **7 User Stories** | **44 Tasks** | **29 Parallelizable** |

---

## Dependencies & Execution Order

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational: Models, Migrations, Infrastructure)
    ↓
Phase 3 (US1 + US2 + US6) ← MVP: Core conversational task management
    ↓
Phase 4 (US7) ← Depends on Phase 3 (conversation persistence)
    ↓
Phase 5 (US3) ← Depends on Phase 3 (task operations)
    ↓
Phase 6 (US4 + US5) ← Depends on Phase 3 (task operations)
    ↓
Phase 7 (Polish & Testing)
```

### Independent Test Criteria

Each user story phase includes independent test criteria to verify completion:

- **US1 (Add Tasks)**: User says "Add a task to buy groceries" → Task created with correct title
- **US2 (View Tasks)**: User asks "What tasks are pending?" → Receives list of incomplete tasks only
- **US6 (Context)**: User creates task, then says "Make that high priority" → System updates the just-created task
- **US7 (Resume)**: User chats, closes interface, reopens → Previous messages still visible
- **US3 (Complete)**: User says "Mark task 3 as complete" → Task status changes to completed
- **US4 (Delete)**: User says "Delete the meeting task" → Task removed from list
- **US5 (Update)**: User says "Change task 1 to high priority" → Task priority updates correctly

---

## Phase 1: Setup & Environment Configuration

**Goal**: Prepare development environment with Phase 3 dependencies and configuration.

**Independent Test**: Backend and frontend servers start without errors, environment variables loaded correctly.

### Tasks

- [X] T001 Update backend pyproject.toml with Phase 3 dependencies in phase-3-ai-todo-chatbot/backend/pyproject.toml
- [X] T002 [P] Update frontend package.json with Phase 3 dependencies in phase-3-ai-todo-chatbot/frontend/package.json
- [X] T003 [P] Update backend .env.example with LLM provider variables in phase-3-ai-todo-chatbot/backend/.env.example
- [X] T004 [P] Update frontend .env.example with ChatKit URL in phase-3-ai-todo-chatbot/frontend/.env.example
- [X] T005 Install dependencies and verify environment setup (backend: uv sync, frontend: npm install)

**Parallel Execution**: Tasks T002, T003, T004 can run in parallel (different files).

**Subagent Recommendation**: Use `backend-expert` for T001, T003 and `frontend-expert` for T002, T004.

---

## Phase 2: Foundational Infrastructure

**Goal**: Implement database models, migrations, and shared infrastructure required by all user stories.

**Independent Test**: Database migration applies successfully, models can be imported without errors, async sessions work correctly.

### Tasks

- [X] T006 [P] Create Conversation model in phase-3-ai-todo-chatbot/backend/src/models/conversation.py
- [X] T007 [P] Create Message model in phase-3-ai-todo-chatbot/backend/src/models/message.py
- [X] T008 Create database migration for conversation and message tables in phase-3-ai-todo-chatbot/backend/alembic/versions/
- [X] T009 Apply database migration (uv run alembic upgrade head)
- [X] T010 [P] Create async database session factory in phase-3-ai-todo-chatbot/backend/src/db/async_session.py
- [X] T011 [P] Create multi-provider LLM factory in phase-3-ai-todo-chatbot/backend/src/agent_config/factory.py
- [X] T012 [P] Create DatabaseStore implementation in phase-3-ai-todo-chatbot/backend/src/services/chatkit_store.py
- [X] T013 [P] Create MemoryStore implementation in phase-3-ai-todo-chatbot/backend/src/services/chatkit_store.py

**Parallel Execution**: Tasks T006, T007, T010, T011, T012, T013 can run in parallel (different files or different classes in same file).

**Subagent Recommendation**: Use `backend-expert` for T006-T010 and `chatkit-backend-engineer` for T011-T013.

**Context7 Research**: Use Context7 to research OpenAI Agents SDK multi-provider configuration and ChatKit Store contracts before implementing T011-T013.

---

## Phase 3: US1 (Add Tasks) + US2 (View Tasks) + US6 (Context) - MVP

**Goal**: Implement core conversational task management with natural language add/view operations and conversation context maintenance.

**Why Combined**: These three user stories form the MVP - users must be able to add tasks, view tasks, and have the system remember context. They are tightly coupled and should be implemented together.

**Independent Test Criteria**:
- US1: User says "Add a task to buy groceries" → Task created with title "Buy groceries"
- US2: User asks "What tasks are pending?" → Receives list of incomplete tasks only
- US6: User creates task, then says "Make that high priority" → System updates the just-created task

### MCP Tools (US1 + US2)

- [X] T014 [P] [US1] Implement add_task MCP tool in phase-3-ai-todo-chatbot/backend/mcp_server/tools.py
- [X] T015 [P] [US2] Implement list_tasks MCP tool in phase-3-ai-todo-chatbot/backend/mcp_server/tools.py
- [X] T016 [P] [US2] Implement get_task MCP tool in phase-3-ai-todo-chatbot/backend/mcp_server/tools.py
- [X] T017 [P] [US1] Implement set_priority MCP tool in phase-3-ai-todo-chatbot/backend/mcp_server/tools.py

### Agent Configuration (US6)

- [X] T018 [US6] Create TodoAgent class with SQLiteSession in phase-3-ai-todo-chatbot/backend/src/agent_config/__init__.py
- [X] T019 [US6] Create TaskChatKitServer with conversation memory in phase-3-ai-todo-chatbot/backend/src/services/chatkit_server.py

### API Endpoint (US1 + US2 + US6)

- [X] T020 [US1] [US2] [US6] Create /api/chatkit endpoint with JWT authentication in phase-3-ai-todo-chatbot/backend/src/api/v1/chatkit.py
- [X] T021 [US1] [US2] [US6] Register chatkit router in main.py at phase-3-ai-todo-chatbot/backend/src/main.py

### Frontend Components (US1 + US2 + US6)

- [X] T022 [P] [US1] [US2] [US6] Create ChatKitWidget component in phase-3-ai-todo-chatbot/frontend/components/chat/chatkit-widget.tsx
- [X] T023 [P] [US1] [US2] [US6] Create GlobalChatButton component in phase-3-ai-todo-chatbot/frontend/components/chat/global-chat-button.tsx
- [X] T024 [US1] [US2] [US6] Integrate GlobalChatButton into dashboard page at phase-3-ai-todo-chatbot/frontend/app/dashboard/page.tsx

### Integration Testing (US1 + US2 + US6)

- [X] T025 [US1] [US2] [US6] Test MVP: Add task via chat, view tasks via chat, verify context maintained across messages

**Parallel Execution**: Tasks T014-T017 (MCP tools), T022-T023 (frontend components) can run in parallel.

**Subagent Recommendation**:
- Use `chatkit-backend-engineer` for T014-T021 (MCP tools, agent, ChatKit server, endpoint)
- Use `chatkit-frontend-engineer` for T022-T024 (ChatKit widget, global button, integration)

**Context7 Research**: Research OpenAI Agents SDK agent configuration, FastMCP tool decorator patterns, and ChatKit React widget setup before implementing.

---

## Phase 4: US7 (Resume Conversations Across Sessions)

**Goal**: Implement conversation persistence so users can close and reopen the chat interface with history intact.

**Independent Test**: User chats, closes interface, reopens → Previous messages still visible.

**Dependencies**: Requires Phase 3 (conversation infrastructure must exist).

### Tasks

- [X] T026 [P] [US7] Implement conversation list endpoint in phase-3-ai-todo-chatbot/backend/src/api/v1/chatkit.py
- [X] T027 [P] [US7] Implement conversation history loading in ChatKitWidget at phase-3-ai-todo-chatbot/frontend/components/chat/chatkit-widget.tsx
- [X] T028 [US7] Test conversation persistence: Chat, close, reopen, verify history intact

**Parallel Execution**: Tasks T026, T027 can run in parallel (backend vs frontend).

**Subagent Recommendation**: Use `chatkit-backend-engineer` for T026 and `chatkit-frontend-engineer` for T027.

---

## Phase 5: US3 (Complete Tasks Conversationally)

**Goal**: Enable users to mark tasks as complete through natural language.

**Independent Test**: User says "Mark task 3 as complete" → Task status changes to completed.

**Dependencies**: Requires Phase 3 (MCP infrastructure and ChatKit endpoint must exist).

### Tasks

- [X] T029 [P] [US3] Implement complete_task MCP tool in phase-3-ai-todo-chatbot/backend/mcp_server/tools.py
- [X] T030 [P] [US3] Update TodoAgent system prompt to handle completion commands in phase-3-ai-todo-chatbot/backend/src/agent_config/__init__.py
- [X] T031 [P] [US3] Add completion command examples to agent instructions in phase-3-ai-todo-chatbot/backend/src/agent_config/__init__.py
- [X] T032 [US3] Test task completion: Say "Mark task 3 as complete", verify task status changes

**Parallel Execution**: Tasks T029, T030, T031 can run in parallel (different functions/sections).

**Subagent Recommendation**: Use `chatkit-backend-engineer` for all tasks in this phase.

---

## Phase 6: US4 (Delete Tasks) + US5 (Update Tasks)

**Goal**: Enable users to delete and update tasks through natural language.

**Why Combined**: Both are P3 features with similar implementation patterns (MCP tools + agent instructions).

**Independent Test Criteria**:
- US4: User says "Delete the meeting task" → Task removed from list
- US5: User says "Change task 1 to high priority" → Task priority updates correctly

**Dependencies**: Requires Phase 3 (MCP infrastructure and ChatKit endpoint must exist).

### Tasks

- [X] T033 [P] [US4] Implement delete_task MCP tool in phase-3-ai-todo-chatbot/backend/mcp_server/tools.py
- [X] T034 [P] [US5] Implement update_task MCP tool in phase-3-ai-todo-chatbot/backend/mcp_server/tools.py
- [X] T035 [P] [US4] Add deletion command examples to agent instructions in phase-3-ai-todo-chatbot/backend/src/agent_config/__init__.py
- [X] T036 [P] [US5] Add update command examples to agent instructions in phase-3-ai-todo-chatbot/backend/src/agent_config/__init__.py
- [X] T037 [US4] Test task deletion: Say "Delete task 5", verify task removed
- [X] T038 [US5] Test task update: Say "Change task 1 to high priority", verify priority updated

**Parallel Execution**: Tasks T033-T036 can run in parallel (different functions/sections).

**Subagent Recommendation**: Use `chatkit-backend-engineer` for all tasks in this phase.

---

## Phase 7: Polish, Testing & Documentation

**Goal**: Comprehensive testing, error handling, and production readiness.

**Independent Test**: All unit tests pass, integration tests pass, user isolation verified, no security vulnerabilities.

### Tasks

- [X] T039 [P] Create unit tests for all MCP tools in phase-3-ai-todo-chatbot/backend/tests/unit/test_mcp_tools.py
- [X] T040 [P] Create unit tests for ChatKit stores in phase-3-ai-todo-chatbot/backend/tests/unit/test_chatkit_store.py
- [X] T041 [P] Create integration tests for ChatKit endpoint in phase-3-ai-todo-chatbot/backend/tests/integration/test_chatkit_endpoint.py
- [X] T042 [P] Create user isolation tests in phase-3-ai-todo-chatbot/backend/tests/integration/test_user_isolation.py
- [X] T043 Run all tests and verify 100% pass rate (uv run pytest)
- [X] T044 Create pull request with implementation summary and testing results

**Parallel Execution**: Tasks T039-T042 can run in parallel (different test files).

**Subagent Recommendation**: Use `chatkit-backend-engineer` for T039-T042, use `sp.git.commit_pr` skill for T044.

---

## Parallel Execution Examples

### Phase 2 Parallelization

Run these tasks concurrently:
```bash
# Terminal 1: Create models
Task T006 + T007 (Conversation and Message models)

# Terminal 2: Create infrastructure
Task T010 (Async sessions)

# Terminal 3: Create agent config
Task T011 (LLM factory)

# Terminal 4: Create stores
Task T012 + T013 (DatabaseStore and MemoryStore)
```

### Phase 3 Parallelization

Run these tasks concurrently:
```bash
# Terminal 1: Backend MCP tools
Task T014 + T015 + T016 + T017 (All MCP tools)

# Terminal 2: Frontend components
Task T022 + T023 (ChatKit widget and global button)

# Terminal 3: Agent configuration
Task T018 + T019 (TodoAgent and TaskChatKitServer)
```

### Phase 7 Parallelization

Run these tasks concurrently:
```bash
# Terminal 1: MCP tool tests
Task T039 (test_mcp_tools.py)

# Terminal 2: Store tests
Task T040 (test_chatkit_store.py)

# Terminal 3: Integration tests
Task T041 (test_chatkit_endpoint.py)

# Terminal 4: Security tests
Task T042 (test_user_isolation.py)
```

---

## Implementation Strategy

### MVP Scope (Recommended First Iteration)

**Phase 1 + Phase 2 + Phase 3** = Minimum Viable Product

This delivers:
- ✅ Add tasks through conversation (US1)
- ✅ View tasks through questions (US2)
- ✅ Conversation context maintenance (US6)
- ✅ Database persistence
- ✅ JWT authentication
- ✅ User isolation

**Estimated Tasks**: 25 tasks (57% of total)

**Independent Test**: User can add tasks, view tasks, and have multi-turn conversations with context maintained.

### Incremental Delivery

After MVP, deliver in priority order:

1. **Phase 4 (US7)**: Resume conversations across sessions - 3 tasks
2. **Phase 5 (US3)**: Complete tasks conversationally - 4 tasks
3. **Phase 6 (US4 + US5)**: Delete and update tasks - 6 tasks
4. **Phase 7**: Polish and comprehensive testing - 6 tasks

Each phase is independently testable and delivers user value.

---

## Validation Checklist

Before marking feature complete, verify:

- [ ] All 44 tasks completed
- [ ] All user stories have independent test criteria verified
- [ ] All MCP tools validate user_id for security
- [ ] Conversation history persists correctly in database
- [ ] JWT authentication works on /api/chatkit endpoint
- [ ] User isolation verified (users cannot access other users' data)
- [ ] Streaming responses work (text appears progressively)
- [ ] All tests pass (unit + integration)
- [ ] No security vulnerabilities detected
- [ ] Documentation updated (README, API docs)

---

## Notes

**Subagent Usage**: Tasks reference specific subagents (backend-expert, chatkit-backend-engineer, etc.) to leverage specialized knowledge. Use the Task tool to invoke these subagents.

**Context7 Research**: Before implementing unfamiliar libraries (OpenAI Agents SDK, FastMCP, ChatKit), use Context7 MCP to research latest documentation and best practices.

**GitHub Integration**: Use GitHub MCP tools for repository operations, branch management, and PR creation.

**Testing Philosophy**: Tests are included in Phase 7 (Polish) rather than TDD approach. This aligns with the spec which doesn't explicitly require TDD.

**User Isolation**: CRITICAL - Every MCP tool MUST validate user_id matches authenticated user. This is enforced in Phase 7 security tests.

**Performance**: Response streaming must start within 1 second (FR-008). Monitor this during integration testing.

---

## Task Format Reference

**Correct Format**:
```
- [ ] T001 Description with file path
- [ ] T002 [P] Description with file path (parallelizable)
- [ ] T003 [P] [US1] Description with file path (parallelizable, user story 1)
- [ ] T004 [US2] Description with file path (user story 2)
```

**Format Rules**:
1. Always start with `- [ ]` (checkbox)
2. Task ID (T001, T002, etc.) in execution order
3. [P] marker ONLY if parallelizable
4. [Story] label (US1, US2, etc.) ONLY for user story phase tasks
5. Clear description with exact file path

---

**Total Tasks**: 44
**Parallelizable Tasks**: 29 (66%)
**User Stories**: 7 (3 P1, 2 P2, 2 P3)
**Phases**: 7

**Status**: Ready for implementation. Start with Phase 1 (Setup).
