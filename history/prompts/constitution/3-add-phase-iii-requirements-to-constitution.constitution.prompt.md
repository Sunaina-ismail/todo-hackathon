---
id: 3
title: Add Phase III Requirements to Constitution
stage: constitution
date: 2026-01-12
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 003-todo-frontend
user: sunaina_ubuntu
command: /sp.constitution
labels: ["constitution", "phase-3", "ai-chatbot", "requirements"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution update)
---

## Prompt

Add a new section "Phase III Mandatory Requirements" immediately after the "Phase II Mandatory Requirements" section. This section MUST include:

AI Chatbot Functionality (All Required)
All AI chatbot features MUST be implemented according to these principles:

Tech Stack: All functionality MUST use the OpenAI Agents SDK, Official MCP Python SDK, openai-chatkit-python (backend), and openai-chatkit-react (frontend).

Conversational Interface: Users MUST be able to manage tasks through natural language conversation.

Natural Language Task Management: All 5 Basic Level features (Add, List, Complete, Delete, Update) MUST work via natural language commands.

Stateless Architecture: Chat endpoints must be completely stateless. Fetch conversation history from the database on every request.

Conversation Persistence & Context: All conversations and messages MUST persist in Neon database tables via openai-chatkit-python to maintain context across multiple messages.

Secure MCP Tools: All MCP tools must be stateless, single-purpose, and reuse existing backend services. Every tool MUST validate that the user_id matches the authenticated user for security.

Error Handling & Feedback: Chatbot MUST provide helpful error messages when commands are not understood and MUST confirm all successful task operations with friendly, deterministic responses.

Reliability: All MCP tools require unit tests and integration tests with a mock agent to ensure they are testable and deterministic.

Keep all existing Phase 1 and Phase 2 principles.

## Response snapshot

Updated constitution from v1.1.0 to v1.2.0 with comprehensive Phase III mandatory requirements. Added new section "Phase III Mandatory Requirements" with 8 core principles covering:

1. **Tech Stack**: Mandated OpenAI Agents SDK, Official MCP Python SDK (FastMCP), openai-chatkit-python, and openai-chatkit-react
2. **Conversational Interface**: Required natural language task management as primary AI interaction method
3. **Natural Language Task Management**: All 5 Basic Level features must work via natural language
4. **Stateless Architecture**: Enforced stateless chat endpoints with database-backed conversation history
5. **Conversation Persistence & Context**: Required Neon database persistence using openai-chatkit-python Store contracts
6. **Secure MCP Tools**: Mandated user_id validation in all MCP tools for security
7. **Error Handling & Feedback**: Required helpful error messages and friendly confirmations
8. **Reliability**: Mandated unit and integration tests for all MCP tools

Version bump rationale: MINOR (1.1.0 → 1.2.0) - Added new requirements section without breaking existing principles.

## Outcome

- ✅ Impact: Constitution updated to v1.2.0 with 8 mandatory Phase III AI chatbot principles
- 🧪 Tests: N/A - Constitution is a governance document
- 📁 Files: Updated .specify/memory/constitution.md with Phase III section
- 🔁 Next prompts: Continue Phase III implementation (models, MCP server, ChatKit integration)
- 🧠 Reflection: Successfully codified Phase III requirements as constitutional mandates, ensuring all AI chatbot work follows OpenAI Agents SDK + MCP + ChatKit stack with proper security and testing

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - Constitution update
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
