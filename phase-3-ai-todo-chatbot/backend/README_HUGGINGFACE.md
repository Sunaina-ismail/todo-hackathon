---
title: Todo App Backend API
emoji: ✅
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🚀 Todo Application - FastAPI Backend

A production-ready FastAPI backend for a full-stack todo application with JWT authentication, PostgreSQL database, and comprehensive task management features.

## ✨ Features

- **RESTful API** - Complete CRUD operations for tasks
- **JWT Authentication** - Secure authentication using shared secret (HS256)
- **User Isolation** - Each user can only access their own tasks
- **Advanced Filtering** - Search, filter by priority/tags, and sort tasks
- **PostgreSQL Database** - Robust data persistence with SQLModel ORM
- **API Documentation** - Auto-generated OpenAPI/Swagger docs
- **Health Checks** - Built-in health monitoring endpoints
- **AI-Powered Chatbot (Phase 3)** - Conversational task management via ChatKit
- **Multi-Provider LLM Support** - OpenAI, Gemini, Groq, OpenRouter
- **MCP Tool Integration** - Model Context Protocol for agent orchestration

## 📋 API Endpoints

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
- `POST /api/chatkit` - ChatKit conversational AI endpoint for task management
- Supports natural language task operations via OpenAI Agents SDK
- Multi-provider LLM support (OpenAI, Gemini, Groq, OpenRouter)

### Health
- `GET /health` - Health check endpoint

## 🔧 Environment Variables

Configure these in your Hugging Face Space settings:

```bash
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require

# Authentication (MUST match frontend)
BETTER_AUTH_SECRET=your_secure_random_secret_min_32_chars
JWT_ALGORITHM=HS256

# CORS (Add your frontend URLs)
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.com

# Server Configuration
PORT=7860
HOST=0.0.0.0
ENVIRONMENT=production

# ============================================================================
# Phase 3: AI Chatbot Configuration (Optional - for ChatKit features)
# ============================================================================

# LLM Provider (choose one: openai | gemini | groq | openrouter)
LLM_PROVIDER=openai

# OpenAI Configuration (Default Provider)
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# Gemini Configuration (Optional - uncomment to use)
# GEMINI_API_KEY=AIza...
# GEMINI_DEFAULT_MODEL=gemini-2.5-flash

# Groq Configuration (Optional - uncomment to use)
# GROQ_API_KEY=gsk_...
# GROQ_DEFAULT_MODEL=llama-3.3-70b-versatile

# OpenRouter Configuration (Optional - uncomment to use)
# OPENROUTER_API_KEY=sk-or-v1-...
# OPENROUTER_DEFAULT_MODEL=openai/gpt-oss-20b:free

# MCP Server Configuration
MCP_SERVER_NAME=todo-task-server
```

**Note**: Phase 3 AI chatbot features are optional. If you don't configure LLM provider settings, the basic task management API will still work perfectly. The ChatKit endpoint requires at least one LLM provider to be configured.

## 🌐 Deploying to Hugging Face Spaces

### Prerequisites

1. **Hugging Face Account** - [Sign up here](https://huggingface.co/join)
2. **Neon Database** - [Create free database](https://neon.tech)
3. **Shared Secret** - Generate: `openssl rand -base64 32`

### Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/new-space)
2. Configure your Space:
   - **Owner**: Your username or organization
   - **Space name**: `todo-app-backend`
   - **License**: MIT
   - **Select SDK**: Docker
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public or Private

3. Click **Create Space**

### Step 2: Set Up Neon Database

1. Go to [Neon Console](https://console.neon.tech)
2. Create a new project: `todo-app-production`
3. Copy the connection string (looks like):
   ```
   postgresql://user:pass@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. Keep this for the next step

### Step 3: Configure Secrets

In your Space, go to **Settings** → **Variables and secrets**:

Add these secrets (click "New secret" for each):

**Required Secrets:**

| Name | Value | Example |
|------|-------|---------|
| `DATABASE_URL` | Your Neon connection string | `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require` |
| `BETTER_AUTH_SECRET` | Random 32+ char string | `dZLDHNC3q5cucIRX1qXkXAMg+y9z8b9IPbI27HnHJosqRgOJrhxby5eUedaltzR7` |
| `ALLOWED_ORIGINS` | Your frontend URLs (comma-separated) | `https://todo-app.vercel.app,https://todo-app-git-main.vercel.app` |
| `PORT` | 7860 (Hugging Face default) | `7860` |
| `ENVIRONMENT` | production | `production` |
| `JWT_ALGORITHM` | HS256 | `HS256` |

**Optional Secrets (Phase 3 AI Chatbot):**

| Name | Value | Example |
|------|-------|---------|
| `LLM_PROVIDER` | LLM provider to use | `openai` (or `gemini`, `groq`, `openrouter`) |
| `OPENAI_API_KEY` | OpenAI API key | `sk-proj-...` |
| `OPENAI_DEFAULT_MODEL` | OpenAI model | `gpt-4o-mini` |
| `GEMINI_API_KEY` | Gemini API key (optional) | `AIza...` |
| `GROQ_API_KEY` | Groq API key (optional) | `gsk_...` |
| `OPENROUTER_API_KEY` | OpenRouter API key (optional) | `sk-or-v1-...` |
| `MCP_SERVER_NAME` | MCP server name | `todo-task-server` |

**Important**:
- Mark all as "Secret" to encrypt them
- Never commit these secrets to your repository
- Phase 3 AI features are optional - basic task management works without them

### Step 4: Upload Files

Upload your backend files to the Space:

```
backend/
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── README.md (this file)
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   ├── auth/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
└── alembic/
    ├── env.py
    ├── script.py.mako
    └── versions/
```

**Methods to upload**:
- **Git**: Clone the Space repo and push your files
- **Web UI**: Drag and drop files in the Space's Files tab
- **Hugging Face CLI**: Use `huggingface-cli upload`

### Step 5: Verify Dockerfile

Ensure your `Dockerfile` exposes port 7860 and runs migrations:

```dockerfile
# Expose Hugging Face default port
EXPOSE 7860

# Run migrations and start server
CMD alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 7860
```

**Important**: The Dockerfile runs database migrations (`alembic upgrade head`) before starting the server. This ensures your database schema is always up to date.

### Step 6: Deploy

1. Commit your files to the Space
2. Hugging Face will automatically:
   - Build the Docker image
   - Run database migrations
   - Start the application
3. Monitor the build in the **Logs** tab
4. Build typically takes 3-5 minutes

### Step 7: Test Your Deployment

Once deployed, your API will be available at:
```
https://YOUR-USERNAME-todo-app-backend.hf.space
```

Test the endpoints:

```bash
# Health check
curl https://YOUR-USERNAME-todo-app-backend.hf.space/health

# API documentation
https://YOUR-USERNAME-todo-app-backend.hf.space/docs
```

## 📚 API Documentation

Access interactive documentation:

- **Swagger UI**: `https://your-space.hf.space/docs`
- **ReDoc**: `https://your-space.hf.space/redoc`

## 🔗 Frontend Integration

Update your frontend environment variables:

```bash
# Vercel, Netlify, or other hosting
NEXT_PUBLIC_API_URL=https://YOUR-USERNAME-todo-app-backend.hf.space
BETTER_AUTH_SECRET=same_secret_as_backend
```

## 🐛 Troubleshooting

### Build Fails

**Problem**: Docker build fails
**Solutions**:
- Check Dockerfile syntax
- Verify `pyproject.toml` has all dependencies
- Review build logs in Space's Logs tab
- Ensure Python version is 3.13+

### Database Connection Error

**Problem**: `connection refused` or `SSL required`
**Solutions**:
- Verify `DATABASE_URL` format is correct
- Ensure `?sslmode=require` is at the end
- Check Neon database is active (not paused)
- Test connection from Neon console

### CORS Errors

**Problem**: Frontend can't access API
**Solutions**:
- Add frontend URL to `ALLOWED_ORIGINS`
- Include both production and preview URLs
- Format: `https://domain1.com,https://domain2.com`
- No trailing slashes in URLs

### JWT Verification Fails

**Problem**: `Invalid token` or `Unauthorized`
**Solutions**:
- Ensure `BETTER_AUTH_SECRET` matches frontend exactly
- Check JWT algorithm is `HS256`
- Verify token is sent in `Authorization: Bearer <token>` header
- Test token at [jwt.io](https://jwt.io)

### Space Sleeping

**Problem**: First request is slow
**Solutions**:
- Hugging Face free tier sleeps after inactivity
- Upgrade to persistent hardware (paid)
- Or accept 10-15 second cold start

### Port Issues

**Problem**: Application not accessible
**Solutions**:
- Ensure Dockerfile exposes port 7860
- Verify `PORT=7860` in environment variables
- Check application binds to `0.0.0.0` not `localhost`

## 📊 Monitoring

Hugging Face provides:

- **Build Logs**: View deployment progress
- **Runtime Logs**: Monitor application logs in real-time
- **Metrics**: CPU and memory usage graphs
- **Health Checks**: Automatic endpoint monitoring

Access logs: Space → **Logs** tab

## 🔄 Updating Your Deployment

To update your backend:

1. Make changes to your code locally
2. Test changes thoroughly
3. Commit and push to the Space repository
4. Hugging Face automatically rebuilds
5. Zero-downtime deployment

## 🔐 Security Best Practices

1. **Secrets Management**
   - Use Hugging Face Secrets for sensitive data
   - Never commit `.env` files
   - Rotate secrets regularly

2. **CORS Configuration**
   - Only allow trusted frontend domains
   - Don't use wildcards (`*`) in production

3. **Database Security**
   - Always use SSL (`?sslmode=require`)
   - Use strong passwords
   - Enable Neon's IP allowlist if needed

4. **JWT Tokens**
   - Use minimum 32-character secrets
   - Set appropriate expiration times
   - Validate all claims

## 💰 Costs

- **Hugging Face**: Free tier available (with sleeping)
- **Neon Database**: Free tier includes 0.5GB storage
- **Upgrade Options**:
  - Persistent hardware: $0.60/hour
  - More storage: Neon Pro plan

## 🌟 Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM with type safety
- **PostgreSQL** - Robust relational database (Neon)
- **Pydantic** - Data validation
- **JWT** - Secure authentication (python-jose)
- **Uvicorn** - Lightning-fast ASGI server
- **Docker** - Containerization
- **Alembic** - Database migrations
- **OpenAI Agents SDK** - AI agent orchestration (Phase 3)
- **ChatKit** - Conversational UI backend (Phase 3)
- **MCP** - Model Context Protocol for tool integration (Phase 3)

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Neon Documentation](https://neon.tech/docs)
- [JWT Best Practices](https://jwt.io/introduction)

## 🤝 Support

- **Issues**: Report on GitHub
- **Discussions**: Hugging Face Community
- **Documentation**: See links above

---

**Built with ❤️ for the Todo Hackathon**

*Deployed on Hugging Face Spaces 🤗*
