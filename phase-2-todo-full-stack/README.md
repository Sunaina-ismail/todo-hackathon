# 🚀 Todo Application - Phase 2

A modern, full-stack todo application with a professional dashboard, real-time analytics, and comprehensive task management features.

## ✨ Features

### Frontend (Next.js 16)
- 🎨 **Professional Dashboard** - Collapsible sidebar, analytics cards, and responsive design
- 📊 **Real-time Analytics** - Task statistics, completion rates, and priority tracking
- 🔍 **Advanced Filtering** - Search, filter by priority/tags, and sort tasks
- 📱 **Fully Responsive** - Mobile-first design with floating action button
- 🎯 **Task Management** - Create, edit, delete, and toggle task completion
- 🏷️ **Tag System** - Organize tasks with custom tags
- 🔐 **Secure Authentication** - Better Auth with JWT tokens

### Backend (FastAPI)
- ⚡ **Fast API** - High-performance Python web framework
- 🔒 **JWT Authentication** - Secure token-based authentication
- 👤 **User Isolation** - Each user can only access their own tasks
- 🗄️ **PostgreSQL Database** - Robust data persistence with SQLModel ORM
- 📝 **API Documentation** - Auto-generated OpenAPI/Swagger docs
- 🏥 **Health Checks** - Built-in monitoring endpoints

## 🏗️ Architecture

```
phase-2-todo-full-stack/
├── frontend/                 # Next.js 16 application
│   ├── app/                 # App Router pages
│   │   ├── dashboard/       # Main dashboard with analytics
│   │   │   ├── page.tsx    # Dashboard overview
│   │   │   ├── tasks/      # Task management page
│   │   │   └── settings/   # Settings page
│   │   ├── sign-in/        # Authentication pages
│   │   └── sign-up/
│   ├── components/          # React components
│   │   ├── dashboard/      # Dashboard components
│   │   │   ├── sidebar.tsx # Collapsible sidebar
│   │   │   └── stat-card.tsx
│   │   ├── tasks/          # Task components
│   │   └── ui/             # shadcn/ui components
│   ├── actions/            # Server actions
│   ├── lib/                # Utilities and config
│   └── Dockerfile          # Frontend Docker config
│
├── backend/                 # FastAPI application
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── auth/           # JWT authentication
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLModel entities
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
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

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd phase-2-todo-full-stack

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

# For local development, these defaults work:
NEXT_PUBLIC_API_URL=http://localhost:8001
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

### 5. Create an Account

1. Navigate to http://localhost:3000
2. Click "Sign Up"
3. Create your account
4. Start managing your tasks!

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
DATABASE_URL=postgresql://user:pass@host:5432/db
BETTER_AUTH_SECRET=your_secret_here
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:3000
PORT=8001
ENVIRONMENT=development
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
DATABASE_URL=postgresql://user:pass@host:5432/db
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
POST   /api/{user_id}/tasks          Create task
GET    /api/{user_id}/tasks          List tasks (with filters)
GET    /api/{user_id}/tasks/{id}     Get task
PATCH  /api/{user_id}/tasks/{id}     Update task
DELETE /api/{user_id}/tasks/{id}     Delete task
GET    /api/{user_id}/tags           Get tags
GET    /health                        Health check
```

## 🎨 Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Authentication**: Better Auth
- **State Management**: React Server Components
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT (python-jose)
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

**Build fails**:
```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for more troubleshooting tips.

## 📊 Features Showcase

### Dashboard
- Welcome message with user's name
- 6 analytics cards (Total, Completion Rate, High Priority, Due Soon, Overdue, Completed)
- Recent tasks preview
- Responsive grid layout

### Sidebar
- Collapsible on desktop (click chevron)
- Floating button on mobile (bottom-right)
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
- User isolation (users can only access their own data)
- CORS configuration
- Environment variable protection
- SQL injection prevention (SQLModel ORM)
- XSS protection (React escaping)
- HTTPS recommended for production

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

---

**Built with ❤️ for the Todo Hackathon**

*Star ⭐ this repo if you find it helpful!*
