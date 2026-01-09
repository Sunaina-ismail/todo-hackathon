# 🚀 Todo Application - Deployment Guide

Complete guide for deploying the Todo Application using Docker, Docker Compose, and Hugging Face Spaces.

## 📋 Table of Contents

- [Quick Start with Docker Compose](#quick-start-with-docker-compose)
- [Environment Setup](#environment-setup)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Hugging Face Deployment](#hugging-face-deployment)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start with Docker Compose

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd phase-2-todo-full-stack
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your values
nano .env
```

**Required variables**:
```bash
# Generate a secure secret (32+ characters)
BETTER_AUTH_SECRET=$(openssl rand -base64 32)

# Database credentials
POSTGRES_PASSWORD=your_secure_password

# For production, use your actual domain
NEXT_PUBLIC_API_URL=http://localhost:8001
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Start All Services

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

### 5. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes data)
docker-compose down -v
```

## 🔧 Environment Setup

### Development Environment

Create `.env` file in the root directory:

```bash
# Database
POSTGRES_DB=todo_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_dev_password
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:your_dev_password@postgres:5432/todo_db

# Authentication
BETTER_AUTH_SECRET=your_32_char_secret_here

# Backend
BACKEND_PORT=8001
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Frontend
FRONTEND_PORT=3000
NEXT_PUBLIC_API_URL=http://localhost:8001
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Production Environment

For production, update these values:

```bash
# Use strong passwords
POSTGRES_PASSWORD=<strong-random-password>
BETTER_AUTH_SECRET=<strong-random-secret>

# Use your actual domains
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
BETTER_AUTH_URL=https://yourdomain.com
NEXT_PUBLIC_APP_URL=https://yourdomain.com
ALLOWED_ORIGINS=https://yourdomain.com

# Use production database (Neon recommended)
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

# Set production environment
ENVIRONMENT=production
```

## 💻 Local Development

### Running Individual Services

#### Backend Only

```bash
cd backend

# Install dependencies
uv sync

# Run migrations
uv run alembic upgrade head

# Start server
uv run uvicorn src.main:app --reload --port 8001
```

#### Frontend Only

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Docker Development

```bash
# Build specific service
docker-compose build backend
docker-compose build frontend

# Start specific service
docker-compose up backend
docker-compose up frontend

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute commands in running container
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🌐 Production Deployment

### Option 1: Docker Compose Production

1. **Prepare production environment**:

```bash
# Create production env file
cp .env.example .env.production

# Edit with production values
nano .env.production
```

2. **Use production compose file**:

```bash
# Build for production
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Option 2: Separate Hosting

#### Backend on Hugging Face Spaces

See [Backend Hugging Face Guide](./backend/README_HUGGINGFACE.md)

**Quick steps**:
1. Create Hugging Face Space with Docker SDK
2. Upload backend files
3. Configure secrets in Space settings
4. Deploy automatically

#### Frontend on Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Set environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://your-backend.hf.space
BETTER_AUTH_SECRET=same_as_backend
DATABASE_URL=your_neon_connection_string
```

#### Frontend on Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy from frontend directory
cd frontend
netlify deploy --prod

# Set environment variables in Netlify dashboard
```

### Option 3: Cloud Platforms

#### AWS ECS/Fargate

```bash
# Build and push images
docker build -t your-registry/todo-backend:latest ./backend
docker build -t your-registry/todo-frontend:latest ./frontend

docker push your-registry/todo-backend:latest
docker push your-registry/todo-frontend:latest

# Deploy using ECS task definitions
```

#### Google Cloud Run

```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/PROJECT-ID/todo-backend ./backend
gcloud run deploy todo-backend --image gcr.io/PROJECT-ID/todo-backend

# Build and deploy frontend
gcloud builds submit --tag gcr.io/PROJECT-ID/todo-frontend ./frontend
gcloud run deploy todo-frontend --image gcr.io/PROJECT-ID/todo-frontend
```

## 🤗 Hugging Face Deployment

### Backend Deployment

Complete guide: [Backend Hugging Face README](./backend/README_HUGGINGFACE.md)

**Summary**:
1. Create Space with Docker SDK
2. Upload backend files
3. Configure environment secrets
4. Automatic deployment

### Frontend Deployment

Hugging Face Spaces also supports Next.js:

1. Create Space with Docker SDK
2. Upload frontend files
3. Configure environment variables
4. Deploy

**Note**: For better performance, consider deploying frontend on Vercel/Netlify.

## 🐛 Troubleshooting

### Docker Issues

**Problem**: Port already in use
```bash
# Find process using port
lsof -i :3000
lsof -i :8001

# Kill process
kill -9 <PID>
```

**Problem**: Permission denied
```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

**Problem**: Out of disk space
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### Database Issues

**Problem**: Connection refused
```bash
# Check if postgres is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart postgres
docker-compose restart postgres
```

**Problem**: Migration fails
```bash
# Reset database (WARNING: deletes data)
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend alembic upgrade head
```

### Build Issues

**Problem**: Frontend build fails
```bash
# Clear Next.js cache
cd frontend
rm -rf .next node_modules
npm install
npm run build
```

**Problem**: Backend build fails
```bash
# Clear Python cache
cd backend
rm -rf .venv __pycache__
uv sync
```

### Network Issues

**Problem**: Services can't communicate
```bash
# Check network
docker network ls
docker network inspect phase-2-todo-full-stack_todo-network

# Recreate network
docker-compose down
docker-compose up
```

## 📊 Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8001/health

# Frontend health
curl http://localhost:3000/api/health

# Database health
docker-compose exec postgres pg_isready
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df

# Detailed info
docker-compose ps
docker-compose top
```

## 🔐 Security Checklist

- [ ] Use strong passwords (20+ characters)
- [ ] Generate secure BETTER_AUTH_SECRET (32+ characters)
- [ ] Enable SSL/TLS in production
- [ ] Configure CORS properly (no wildcards)
- [ ] Use environment variables for secrets
- [ ] Enable database SSL (sslmode=require)
- [ ] Regular security updates
- [ ] Implement rate limiting
- [ ] Enable firewall rules
- [ ] Regular backups

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Documentation](https://docs.docker.com/compose)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)

## 🤝 Support

- **Issues**: Create GitHub issue
- **Discussions**: GitHub Discussions
- **Documentation**: See links above

---

**Built with ❤️ for the Todo Hackathon**
