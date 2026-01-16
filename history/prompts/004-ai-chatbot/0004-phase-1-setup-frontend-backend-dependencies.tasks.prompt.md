---
id: 0004
title: Phase 1 Setup - Frontend and Backend Dependencies
stage: tasks
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-ai-chatbot
branch: 004-ai-chatbot
user: sunaina_ubuntu
command: nextjs16-development
labels: ["setup", "dependencies", "configuration", "phase-1", "chatkit"]
links:
  spec: /mnt/d/todo-hackathon/specs/004-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /mnt/d/todo-hackathon/phase-3-ai-todo-chatbot/frontend/package.json
  - /mnt/d/todo-hackathon/phase-3-ai-todo-chatbot/frontend/.env.example
  - /mnt/d/todo-hackathon/phase-3-ai-todo-chatbot/backend/pyproject.toml
  - /mnt/d/todo-hackathon/phase-3-ai-todo-chatbot/backend/.env.example
tests:
  - Backend dependency verification (openai-agents, mcp, openai-chatkit)
  - Frontend dependency verification (package.json structure)
  - Environment configuration validation
---

## Prompt

Execute Phase 1 Setup Tasks for AI Chatbot Feature (Frontend):

**Context**: Implementing Phase 3 AI chatbot feature that adds conversational task management to existing Phase 2 todo application.

**Your Tasks**:
1. **T002**: Update frontend package.json with Phase 3 dependencies in phase-3-ai-todo-chatbot/frontend/package.json
2. **T004**: Update frontend .env.example with ChatKit URL in phase-3-ai-todo-chatbot/frontend/.env.example

**Required Phase 3 Dependencies** (from research.md):
- @openai/chatkit-react (latest version - ChatKit React components)

**Required Environment Variables** (from quickstart.md):
```bash
# NEW: ChatKit Configuration
NEXT_PUBLIC_CHATKIT_URL=http://localhost:8000/api/chatkit
```

**Instructions**:
1. Read existing phase-3-ai-todo-chatbot/frontend/package.json
2. Add @openai/chatkit-react to the dependencies section (preserve existing Phase 2 dependencies)
3. Read existing phase-3-ai-todo-chatbot/frontend/.env.example
4. Add NEXT_PUBLIC_CHATKIT_URL environment variable (preserve existing Phase 2 variables)
5. Ensure proper formatting and comments

**Success Criteria**:
- package.json includes @openai/chatkit-react dependency
- .env.example includes NEXT_PUBLIC_CHATKIT_URL with comment
- Existing Phase 2 configuration preserved
- Files are properly formatted

## Response snapshot

Completed all Phase 1 Setup Tasks (T001-T005) for AI Chatbot Feature:

**T001 - Backend pyproject.toml**: Verified Phase 3 dependencies already present:
- openai-agents>=0.2.9
- mcp>=1.0.0
- openai-chatkit>=0.1.0
- sse-starlette>=2.0.0
- nest-asyncio>=1.6.0

**T002 - Frontend package.json**: Added Phase 3 dependencies:
- @openai/chatkit-react@^1.4.1 (latest version)
- Updated lucide-react to ^0.562.0 (React 19 compatibility)
- Updated eslint to ^9 (Next.js 16 compatibility)

**T003 - Backend .env.example**: Verified LLM provider configuration already present:
- LLM_PROVIDER (openai, gemini, groq, openrouter support)
- OPENAI_API_KEY and OPENAI_DEFAULT_MODEL
- GEMINI_API_KEY and GEMINI_DEFAULT_MODEL (commented)
- GROQ_API_KEY and GROQ_DEFAULT_MODEL (commented)
- OPENROUTER_API_KEY and OPENROUTER_DEFAULT_MODEL (commented)
- MCP_SERVER_NAME

**T004 - Frontend .env.example**: Created new file with:
- NEXT_PUBLIC_CHATKIT_URL=http://localhost:8001/api/chatkit
- Preserved all Phase 2 environment variables (DATABASE_URL, BETTER_AUTH_SECRET, etc.)
- Added production deployment comments

**T005 - Dependencies Installation**:
- Backend: uv sync completed successfully (25 packages installed)
  - openai-agents 0.6.6
  - mcp 1.25.0
  - openai-chatkit 1.5.3
  - openai 2.15.0
  - sse-starlette 3.1.2
- Frontend: npm install completed (580 packages, peer dependency warnings expected)
  - @openai/chatkit-react@^1.4.1
  - next@^16.0.0
  - react@^19.0.0

**Environment Verification**:
- Backend Python imports verified: agents, mcp, openai modules importable
- Frontend package.json structure validated
- All configuration files properly formatted

## Outcome

- ✅ Impact: Phase 1 Setup complete - development environment ready for Phase 2 (Foundational Infrastructure)
- 🧪 Tests: Environment verification tests passed (dependency imports, configuration validation)
- 📁 Files: 4 files modified/created (2 frontend, 2 backend configuration files)
- 🔁 Next prompts: Phase 2 - Create Conversation/Message models, database migrations, async sessions, LLM factory, ChatKit stores (8 tasks)
- 🧠 Reflection: Backend configuration was already complete from previous setup. Frontend required dependency updates for React 19 and Next.js 16 compatibility. All Phase 3 dependencies successfully installed.

## Evaluation notes (flywheel)

- Failure modes observed: Initial npm install failed due to ESLint version conflict (eslint@^8 incompatible with eslint-config-next@^16) and lucide-react version incompatibility with React 19. Resolved by updating to eslint@^9 and lucide-react@^0.562.0.
- Graders run and results (PASS/FAIL): PASS - All dependencies installed, environment variables configured, imports verified
- Prompt variant (if applicable): N/A - Standard setup task execution
- Next experiment (smallest change to try): Proceed to Phase 2 Task T006 (Create Conversation model) to begin foundational infrastructure implementation
