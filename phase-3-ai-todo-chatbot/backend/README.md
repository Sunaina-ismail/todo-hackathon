---
title: Todo App Backend API
emoji: ✅
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🚀 Todo Application - FastAPI Backend (Phase 3)

Production-ready FastAPI backend with JWT authentication, PostgreSQL database, and AI-powered conversational task management via ChatKit.

## ✨ Features

- **RESTful API** - Complete CRUD operations for tasks
- **JWT Authentication** - Secure authentication using shared secret (HS256)
- **User Isolation** - Each user can only access their own tasks
- **Advanced Filtering** - Search, filter by priority/tags, and sort tasks
- **PostgreSQL Database** - Robust data persistence with SQLModel ORM
- **API Documentation** - Auto-generated OpenAPI/Swagger docs
- **Health Checks** - Built-in health monitoring endpoints
- **AI-Powered Chatbot** - Conversational task management via ChatKit
- **Multi-Provider LLM** - OpenAI, Gemini, Groq, OpenRouter support
- **MCP Tool Integration** - Model Context Protocol for agent orchestration

## 📋 API Endpoints

### Core Endpoints
- `GET /health` - Health check (no auth required)
- `GET /` - API information
- `GET /docs` - Interactive API documentation

### Authentication
- `POST /api/auth/verify` - Verify JWT token

### Tasks
- `GET /api/{user_id}/tasks` - List all tasks (with filters)
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get task by ID
- `PATCH /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task

### Tags
- `GET /api/{user_id}/tags` - Get user's tags with usage counts

### AI Chatbot (Phase 3)
- `POST /api/chatkit` - ChatKit conversational AI endpoint
  - Natural language task operations
  - Multi-provider LLM support
  - Conversation history management

## 🔧 Environment Variables

Configure these in **Settings → Variables and secrets**:

### Required Variables
```bash
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
BETTER_AUTH_SECRET=your_secure_random_secret_min_32_chars
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=https://your-frontend.vercel.app
PORT=7860
HOST=0.0.0.0
ENVIRONMENT=production
```

### Optional Variables (Phase 3 AI Features)
```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_DEFAULT_MODEL=openai/gpt-4o-mini
MCP_SERVER_NAME=todo-task-server
```

**Note**: Phase 3 AI features are optional. Basic task management works without them.

## 🚀 Quick Start

Once deployed, your API will be available at:
- **API**: `https://huggingface.co/spaces/Sunaina1/todo-phase3`
- **Docs**: `https://sunaina1-todo-phase3.hf.space/docs`
- **Health**: `https://sunaina1-todo-phase3.hf.space/health`

## 🏗️ Tech Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel 0.0.22+
- **Authentication**: JWT (HS256)
- **Migrations**: Alembic 1.13+
- **AI Agent**: OpenAI Agents SDK 0.2.9+
- **MCP Protocol**: MCP 1.0.0+
- **ChatKit**: OpenAI ChatKit 0.1.0+
- **Python**: 3.13+
- **Package Manager**: UV

## 🐛 Troubleshooting

### Build Fails
- Ensure all files are uploaded (Dockerfile, pyproject.toml, uv.lock, src/, alembic/)
- Check Dockerfile syntax
- Verify environment variables are set

### Database Connection Fails
- Ensure `?sslmode=require` is in DATABASE_URL
- Check Neon database is active (not paused)

### CORS Errors
- Add frontend URL to ALLOWED_ORIGINS
- No trailing slashes in URLs

### JWT Verification Fails
- BETTER_AUTH_SECRET must match frontend exactly
- Check for extra spaces or line breaks

## 💰 Cost

**Free Tier**:
- Hugging Face: Free (with cold starts)
- Neon: Free (0.5GB storage)

**Total: $0/month** + LLM API costs (if using Phase 3 features)

## 📞 Support

- **Hugging Face**: [discuss.huggingface.co](https://discuss.huggingface.co)
- **Neon**: [neon.tech/discord](https://neon.tech/discord)

---

**Built with ❤️ for the Todo Hackathon**

*Deployed on Hugging Face Spaces 🤗*
