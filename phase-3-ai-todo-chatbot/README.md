# 🤖 Todo Application - Phase 3 (AI-Powered Chatbot)

A modern, full-stack todo application with **AI-powered natural language task management**, professional dashboard, real-time analytics, and comprehensive task management features.

## ✨ Features

### 🤖 Phase 3: AI Chatbot (NEW!)
- 💬 **Natural Language Interface** - Manage tasks through conversational AI
- 🧠 **Multi-Provider LLM Support** - OpenAI, Gemini, Groq, or OpenRouter
- 🔧 **MCP Tool Integration** - Model Context Protocol for task operations
- 💾 **Conversation Memory** - Persistent chat history with SQLite sessions
- ⚡ **Streaming Responses** - Real-time AI responses via Server-Sent Events
- 🎯 **Smart Task Creation** - Auto-detect priority and due dates from natural language
- 📊 **Context-Aware** - AI remembers conversation history for better assistance

### Frontend (Next.js 16)
- 🎨 **Professional Dashboard** - Collapsible sidebar, analytics cards, and responsive design
- 💬 **ChatKit Widget** - Floating AI assistant button with modal chat interface
- 📊 **Real-time Analytics** - Task statistics, completion rates, and priority tracking
- 🔍 **Advanced Filtering** - Search, filter by priority/tags, and sort tasks
- 📱 **Fully Responsive** - Mobile-first design with proper hamburger menu placement
- 🎯 **Task Management** - Create, edit, delete, and toggle task completion
- 🏷️ **Tag System** - Organize tasks with custom tags
- 🔐 **Secure Authentication** - Better Auth with JWT tokens

### Backend (FastAPI)
- ⚡ **Fast API** - High-performance Python web framework
- 🤖 **OpenAI Agents SDK** - AI agent orchestration with tool calling
- 🔧 **MCP Server** - FastMCP tools for task operations (add, list, complete, delete, update)
- 🔒 **JWT Authentication** - Secure token-based authentication
- 👤 **User Isolation** - Each user can only access their own tasks and conversations
- 🗄️ **PostgreSQL Database** - Robust data persistence with SQLModel ORM
- 💬 **ChatKit Protocol** - Official OpenAI ChatKit server implementation
- 📝 **API Documentation** - Auto-generated OpenAPI/Swagger docs
- 🏥 **Health Checks** - Built-in monitoring endpoints

## 🏗️ Architecture

```
phase-3-ai-todo-chatbot/
├── frontend/                 # Next.js 16 application
│   ├── app/                 # App Router pages
│   │   ├── dashboard/       # Main dashboard with analytics
│   │   │   ├── page.tsx    # Dashboard overview
│   │   │   ├── tasks/      # Task management page
│   │   │   └── settings/   # Settings page
│   │   ├── sign-in/        # Authentication pages
│   │   └── sign-up/
│   ├── components/          # React components
│   │   ├── chat/           # ChatKit widget and global chat button
│   │   ├── layout/         # Responsive sidebar and dashboard layout
│   │   ├── tasks/          # Task components
│   │   └── ui/             # shadcn/ui components
│   ├── actions/            # Server actions
│   ├── lib/                # Utilities and config
│   └── Dockerfile          # Frontend Docker config
│
├── backend/                 # FastAPI application
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   │   └── v1/
│   │   │       ├── tasks.py    # Task CRUD endpoints
│   │   │       ├── tags.py     # Tag endpoints
│   │   │       └── chatkit.py  # ChatKit protocol endpoint
│   │   ├── auth/           # JWT authentication
│   │   ├── db/             # Database configuration (lazy loading)
│   │   ├── models/         # SQLModel entities (Task, Conversation, Message)
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── task_service.py      # Task operations
│   │   │   ├── chatkit_server.py    # ChatKit server implementation
│   │   │   └── chatkit_store.py     # ChatKit memory store
│   │   └── agent_config/   # AI agent configuration
│   │       ├── factory.py          # Multi-provider LLM factory
│   │       └── todo_agent.py       # TodoAgent with MCP integration
│   ├── mcp_server/         # MCP tools for AI agent
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── tools.py        # FastMCP tools (add_task, list_tasks, etc.)
│   ├── alembic/            # Database migrations
│   ├── Dockerfile          # Backend Docker config
│   └── README_HUGGINGFACE.md
│
├── docker-compose.yml       # Development setup
├── docker-compose.prod.yml  # Production setup
├── .env.example            # Environment template
├── DEPLOYMENT.md           # Deployment guide
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Node.js** 20+ (for local development)
- **Python** 3.13+ (for local development)
- **LLM API Key** - At least one of: OpenAI, Gemini, Groq, or OpenRouter

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd phase-3-ai-todo-chatbot

# Copy environment template
cp .env.example .env

# Generate secure secret
openssl rand -base64 32
# Copy the output and paste it as BETTER_AUTH_SECRET in .env
```

### 2. Configure Environment

Edit `.env` file:

```bash
# Required: Generate a secure secret (32+ characters)
BETTER_AUTH_SECRET=your_generated_secret_here

# Database credentials
POSTGRES_PASSWORD=your_secure_password

# Phase 3: AI Chatbot Configuration
# Choose your LLM provider (openai|gemini|groq|openrouter)
LLM_PROVIDER=openai

# OpenAI (recommended for best quality)
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# OR Gemini (Google's LLM)
# GEMINI_API_KEY=AIza...
# GEMINI_DEFAULT_MODEL=gemini-2.0-flash-exp

# OR Groq (fastest inference)
# GROQ_API_KEY=gsk_...
# GROQ_DEFAULT_MODEL=llama-3.3-70b-versatile

# OR OpenRouter (multi-model access + free tier)
# OPENROUTER_API_KEY=sk-or-v1-...
# OPENROUTER_DEFAULT_MODEL=openai/gpt-4o-mini

# For local development, these defaults work:
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_CHATKIT_URL=http://localhost:8001/api/chatkit
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Database**: localhost:5432

### 5. Create an Account & Try the AI Chatbot

1. Navigate to http://localhost:3000
2. Click "Sign Up" and create your account
3. Click the **purple chat button** (bottom-right) to open the AI assistant
4. Try natural language commands:
   - "Add a task to buy groceries"
   - "Show my high priority tasks"
   - "Mark task 1 as complete"
   - "What tasks are due soon?"

## 💻 Local Development

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

### Backend Development

```bash
cd backend

# Install dependencies
uv sync

# Run migrations
uv run alembic upgrade head

# Start development server
uv run uvicorn src.main:app --reload --port 8001

# Run tests
uv run pytest

# Type checking
uv run mypy src/ --strict
```

### Testing the AI Chatbot Locally

```bash
# Terminal 1: Start backend
cd backend
uv run uvicorn src.main:app --reload --port 8001

# Terminal 2: Start frontend
cd frontend
npm run dev

# Open http://localhost:3000 and click the chat button
```

## 🌐 Deployment

### Option 1: Docker Compose (Recommended)

**Development**:
```bash
docker-compose up --build
```

**Production**:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### Option 2: Separate Hosting

**Backend on Hugging Face Spaces**:
- See [Backend Hugging Face Guide](./backend/README_HUGGINGFACE.md)
- Free tier available with Docker SDK
- Automatic deployment from Git
- **Note**: Set LLM_PROVIDER and API keys in Space secrets

**Frontend on Vercel**:
```bash
cd frontend
vercel deploy --prod
```

**Frontend on Netlify**:
```bash
cd frontend
netlify deploy --prod
```

### Complete Deployment Guide

See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive deployment instructions including:
- Docker Compose setup
- Cloud platform deployment (AWS, GCP, Azure)
- Hugging Face Spaces deployment
- Environment configuration
- Troubleshooting

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Authentication
BETTER_AUTH_SECRET=your_secret_here
JWT_ALGORITHM=HS256

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Server
PORT=8001
ENVIRONMENT=development

# Phase 3: AI Chatbot
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# Optional: Other providers
GEMINI_API_KEY=AIza...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-v1-...
```

#### Frontend (.env.local)
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_CHATKIT_URL=http://localhost:8001/api/chatkit

# Database (for Better Auth)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Authentication
BETTER_AUTH_SECRET=same_as_backend
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 📚 API Documentation

Once the backend is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Key Endpoints

```
# Task Management
POST   /api/{user_id}/tasks          Create task
GET    /api/{user_id}/tasks          List tasks (with filters)
GET    /api/{user_id}/tasks/{id}     Get task
PATCH  /api/{user_id}/tasks/{id}     Update task
DELETE /api/{user_id}/tasks/{id}     Delete task
GET    /api/{user_id}/tags           Get tags

# Phase 3: AI Chatbot
POST   /api/chatkit                   ChatKit protocol endpoint (SSE streaming)

# Health
GET    /health                        Health check
```

## 🎨 Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Authentication**: Better Auth
- **AI Chat**: OpenAI ChatKit Widget
- **Animations**: Framer Motion
- **State Management**: React Server Components
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT (python-jose)
- **AI Agent**: OpenAI Agents SDK
- **MCP Server**: FastMCP
- **LLM Providers**: OpenAI, Gemini, Groq, OpenRouter
- **Chat Protocol**: ChatKit
- **Migrations**: Alembic
- **Package Manager**: UV

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions (optional)
- **Hosting**: Hugging Face Spaces, Vercel, Netlify

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm test
npm run test:e2e
```

### Backend Tests
```bash
cd backend
uv run pytest
uv run pytest --cov=src --cov-report=html
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use**:
```bash
# Find and kill process
lsof -i :3000
lsof -i :8001
kill -9 <PID>
```

**Database connection error**:
```bash
# Check if postgres is running
docker-compose ps postgres

# Restart postgres
docker-compose restart postgres
```

**AI Chatbot timeout**:
```bash
# Check backend logs
docker-compose logs backend

# Verify LLM API key is set
echo $OPENAI_API_KEY

# Restart backend
docker-compose restart backend
```

**MCP server not responding**:
```bash
# Check if MCP server subprocess is running
ps aux | grep mcp_server

# Restart backend to clear stale processes
docker-compose restart backend
```

**Build fails**:
```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for more troubleshooting tips.

## 📊 Features Showcase

### AI Chatbot
- Natural language task management
- Conversational interface with memory
- Auto-detect priority from keywords (urgent, important, etc.)
- Natural date parsing ("tomorrow", "next friday", "in 3 days")
- Context-aware responses
- Streaming responses for real-time feedback
- Floating chat button with modal interface

### Dashboard
- Welcome message with user's name
- 6 analytics cards (Total, Completion Rate, High Priority, Due Soon, Overdue, Completed)
- Recent tasks preview
- Responsive grid layout

### Sidebar
- Collapsible on desktop (click chevron)
- Slides in from left on mobile (hamburger menu in top-left)
- Active route highlighting
- User profile section
- Sign out functionality

### Task Management
- Create tasks with title, description, priority, due date, and tags
- Search tasks by title/description
- Filter by priority (High/Medium/Low)
- Filter by tags
- Sort by created date, due date, priority, or title
- Edit and delete tasks
- Toggle completion status
- Pagination for large lists

## 🔐 Security

- JWT token-based authentication
- User isolation (users can only access their own data and conversations)
- CORS configuration
- Environment variable protection
- SQL injection prevention (SQLModel ORM)
- XSS protection (React escaping)
- HTTPS recommended for production
- LLM API keys stored securely in environment variables

## 🤖 AI Chatbot Examples

### Natural Language Commands

**Creating Tasks**:
- "Add a task to buy groceries"
- "Remind me to call mom tomorrow"
- "Create a high priority task to finish the report by Friday"
- "Add task: prepare presentation, due next monday"

**Listing Tasks**:
- "Show my tasks"
- "What are my high priority tasks?"
- "List all pending tasks"
- "Show tasks due this week"

**Completing Tasks**:
- "Mark task 1 as complete"
- "I finished buying groceries"
- "Complete the report task"

**Updating Tasks**:
- "Change task 2 to high priority"
- "Update task 3 title to 'Buy groceries and cook dinner'"
- "Set the due date for task 1 to tomorrow"

**Deleting Tasks**:
- "Delete task 5"
- "Remove the meeting task"

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📞 Support

- **Documentation**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Issues**: Create a GitHub issue
- **Discussions**: GitHub Discussions

## 🌟 Acknowledgments

- Built with [Next.js](https://nextjs.org)
- Powered by [FastAPI](https://fastapi.tiangolo.com)
- UI components from [shadcn/ui](https://ui.shadcn.com)
- Database by [Neon](https://neon.tech)
- Authentication by [Better Auth](https://www.better-auth.com)
- AI powered by [OpenAI Agents SDK](https://github.com/openai/openai-agents-sdk)
- Chat interface by [OpenAI ChatKit](https://platform.openai.com/docs/chatkit)
- Tool orchestration by [FastMCP](https://github.com/jlowin/fastmcp)

---

**Built with ❤️ for the Todo Hackathon - Phase 3: AI-Powered Chatbot**

*Star ⭐ this repo if you find it helpful!*
