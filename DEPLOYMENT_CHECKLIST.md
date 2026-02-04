# 🚀 Complete Deployment Checklist

## ✅ Build Verification Status

### Frontend Build
```
✓ Compiled successfully in 92s
✓ TypeScript: 0 errors
✓ All routes generated: 9/9
✓ Production build: READY
```

### Backend Configuration
```
✓ Dockerfile: Configured for Hugging Face (port 7860)
✓ Dependencies: All listed in pyproject.toml
✓ Database migrations: Alembic configured
✓ Health check: Implemented
```

## 📋 Pre-Deployment Requirements

### 1. Accounts & Services

- [ ] **GitHub Account** - For code repository
- [ ] **Vercel Account** - For frontend hosting ([Sign up](https://vercel.com/signup))
- [ ] **Hugging Face Account** - For backend hosting ([Sign up](https://huggingface.co/join))
- [ ] **Neon Account** - For PostgreSQL database ([Sign up](https://neon.tech))

### 2. Generate Secrets

Generate a secure secret for JWT authentication:

```bash
# Generate 32+ character secret
openssl rand -base64 32

# Example output:
# dZLDHNC3q5cucIRX1qXkXAMg+y9z8b9IPbI27HnHJosqRgOJrhxby5eUedaltzR7

# Save this - you'll use it for BOTH frontend and backend!
```

**Critical**: This secret MUST be identical on both frontend and backend!

## 🗄️ Step 1: Database Setup (Neon PostgreSQL)

### 1.1 Create Database

1. Go to [Neon Console](https://console.neon.tech)
2. Click **"Create Project"**
3. Configure:
   - **Project name**: `todo-app-production`
   - **Region**: Choose closest to your users
   - **PostgreSQL version**: 16 (latest)
4. Click **"Create Project"**

### 1.2 Get Connection String

1. In project dashboard, click **"Connection Details"**
2. Copy the connection string:
   ```
   postgresql://user:password@ep-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```
3. **Save this** - you'll need it for both frontend and backend

### 1.3 Verify Connection

Test the connection:
```bash
psql "postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require"
```

Expected: Successfully connected to database

## 🔧 Step 2: Backend Deployment (Hugging Face)

### 2.1 Create Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/new-space)
2. Configure:
   - **Owner**: Your username
   - **Space name**: `todo-app-backend`
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU basic (free)
   - **Visibility**: Public or Private
3. Click **"Create Space"**

### 2.2 Configure Environment Variables

In your Space → **Settings** → **Variables and secrets**, add:

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | Your Neon connection string | Include `?sslmode=require` |
| `BETTER_AUTH_SECRET` | Your generated secret | Must be 32+ characters |
| `ALLOWED_ORIGINS` | `https://your-app.vercel.app` | Update after frontend deployment |
| `PORT` | `7860` | Hugging Face default |
| `ENVIRONMENT` | `production` | Production mode |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |

**Important**: Mark all as "Secret" to encrypt them!

### 2.3 Upload Backend Files

Upload these files to your Space:

```
backend/
├── Dockerfile ✓
├── pyproject.toml ✓
├── uv.lock ✓
├── README.md
├── alembic.ini
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

**Methods**:
- **Git**: Clone Space repo, copy files, push
- **Web UI**: Drag and drop in Files tab
- **CLI**: `huggingface-cli upload`

### 2.4 Monitor Deployment

1. Go to **Logs** tab
2. Watch build progress
3. Wait for: `Application startup complete`
4. Build takes ~3-5 minutes

### 2.5 Verify Backend

Test your backend:

```bash
# Health check
curl https://YOUR-USERNAME-todo-app-backend.hf.space/health

# Expected response:
# {"status":"healthy","database":"connected"}

# API docs
# Visit: https://YOUR-USERNAME-todo-app-backend.hf.space/docs
```

**Save your backend URL** - you'll need it for frontend!

## 🌐 Step 3: Frontend Deployment (Vercel)

### 3.1 Push to GitHub

```bash
# Navigate to project root
cd /mnt/d/todo-hackathon

# Initialize git (if not already done)
git init
git add .
git commit -m "feat: ready for production deployment"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR-USERNAME/todo-app.git
git branch -M main
git push -u origin main
```

### 3.2 Import to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Click **"Import Project"**
3. Select your GitHub repository
4. Configure:
   - **Framework**: Next.js (auto-detected)
   - **Root Directory**: `phase-3-ai-todo-chatbot/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

### 3.3 Configure Environment Variables

In Vercel → **Settings** → **Environment Variables**, add:

| Variable | Value | Example |
|----------|-------|---------|
| `NEXT_PUBLIC_API_URL` | Your Hugging Face backend URL | `https://username-todo-backend.hf.space` |
| `BETTER_AUTH_SECRET` | **Same secret as backend** | `dZLDHNC3q5cucIRX1qXk...` |
| `BETTER_AUTH_URL` | Your Vercel URL (update after deploy) | `https://todo-app.vercel.app` |
| `DATABASE_URL` | Same Neon database URL | `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require` |

**Important**:
- Add for **Production**, **Preview**, and **Development**
- `BETTER_AUTH_SECRET` must match backend exactly!

### 3.4 Deploy

1. Click **"Deploy"**
2. Wait for build (~2-3 minutes)
3. Get your Vercel URL: `https://your-project.vercel.app`

### 3.5 Update Backend CORS

Now that you have your Vercel URL:

1. Go back to Hugging Face Space
2. **Settings** → **Variables and secrets**
3. Update `ALLOWED_ORIGINS`:
   ```
   https://your-project.vercel.app,https://your-project-git-main.vercel.app
   ```
4. Space will automatically restart

### 3.6 Update Frontend URL

1. Go to Vercel → **Settings** → **Environment Variables**
2. Update `BETTER_AUTH_URL` with your actual Vercel URL
3. Click **"Redeploy"** to apply changes

## 🧪 Step 4: Testing

### 4.1 Backend Tests

```bash
# Health check
curl https://YOUR-USERNAME-todo-backend.hf.space/health

# API documentation
# Visit: https://YOUR-USERNAME-todo-backend.hf.space/docs
```

Expected:
- ✅ Health check returns `{"status":"healthy"}`
- ✅ API docs page loads
- ✅ No errors in Space logs

### 4.2 Frontend Tests

Visit: `https://your-project.vercel.app`

**Test Checklist**:
- [ ] Landing page loads
- [ ] Sign up works (create test account)
- [ ] Sign in works
- [ ] Dashboard loads with all 6 cards
- [ ] All 4 charts render
- [ ] Navigate to Tasks page
- [ ] Create a new task
- [ ] Edit a task
- [ ] Delete a task
- [ ] Sort tasks (Date Created, Priority, etc.)
- [ ] Filter tasks (Status, Priority)
- [ ] Search tasks
- [ ] No console errors

### 4.3 Integration Tests

Test the full flow:

1. **Sign Up** → Should create account and redirect to dashboard
2. **Dashboard** → Should show 0 tasks initially
3. **Create Task** → Should appear in dashboard stats
4. **Complete Task** → Should update completion rate
5. **Sign Out** → Should redirect to landing page
6. **Sign In** → Should see your tasks

## 🐛 Common Issues & Solutions

### Issue 1: CORS Errors

**Symptom**: Console shows `Access-Control-Allow-Origin` errors

**Solution**:
```bash
# Backend ALLOWED_ORIGINS must include frontend URL
# Format: https://domain1.com,https://domain2.com
# No trailing slashes!
```

### Issue 2: Authentication Fails

**Symptom**: Can't sign in, "Invalid token" errors

**Solution**:
- Verify `BETTER_AUTH_SECRET` is **identical** on frontend and backend
- Check it's at least 32 characters
- No extra spaces or line breaks

### Issue 3: Database Connection Fails

**Symptom**: Backend logs show "connection refused"

**Solution**:
- Verify `DATABASE_URL` includes `?sslmode=require`
- Check Neon database is active (not paused)
- Test connection from Neon console

### Issue 4: Build Fails

**Symptom**: Vercel or Hugging Face build fails

**Solution**:
- Check build logs for specific errors
- Verify all dependencies are listed
- Test build locally first: `npm run build`

### Issue 5: Slow First Load

**Symptom**: First request takes 10-15 seconds

**Solution**:
- This is normal for free tier (cold start)
- Hugging Face Spaces sleep after inactivity
- Subsequent requests are fast
- Upgrade to persistent hardware if needed

## 📊 Monitoring

### Vercel Monitoring

Access: Vercel Dashboard → Your Project

- **Analytics**: Page views, performance
- **Logs**: Real-time function logs
- **Speed Insights**: Core Web Vitals
- **Deployments**: History and status

### Hugging Face Monitoring

Access: Your Space → Logs tab

- **Build Logs**: Deployment progress
- **Runtime Logs**: Application logs
- **Metrics**: CPU and memory usage
- **Health**: Automatic endpoint checks

## 🔐 Security Checklist

- [ ] `BETTER_AUTH_SECRET` is 32+ characters
- [ ] All secrets stored in platform secrets (not in code)
- [ ] Database uses SSL (`?sslmode=require`)
- [ ] CORS only allows trusted domains
- [ ] No `.env` files committed to git
- [ ] Strong database password
- [ ] JWT tokens have expiration
- [ ] HTTPS enabled (automatic on both platforms)

## 💰 Cost Summary

### Free Tier (Perfect for Testing)

- **Vercel Hobby**: Free
  - 100GB bandwidth/month
  - Unlimited deployments
  - Automatic HTTPS

- **Hugging Face**: Free
  - CPU basic hardware
  - Sleeps after inactivity
  - 10-15 second cold start

- **Neon**: Free
  - 0.5GB storage
  - 1 project
  - Auto-pause after inactivity

**Total**: $0/month for testing and personal use

### Production Tier (For Real Users)

- **Vercel Pro**: $20/month
  - 1TB bandwidth
  - Team features
  - Advanced analytics

- **Hugging Face**: ~$0.60/hour
  - Persistent hardware
  - No cold starts
  - Better performance

- **Neon Pro**: $19/month
  - 10GB storage
  - Multiple projects
  - Always active

**Total**: ~$40-60/month for production

## 📖 Documentation Links

### Platform Docs
- [Vercel Documentation](https://vercel.com/docs)
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
- [Neon Documentation](https://neon.tech/docs)

### Framework Docs
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Better Auth](https://www.better-auth.com/docs)

### Guides
- Frontend: `frontend/DEPLOYMENT.md`
- Backend: `backend/README_HUGGINGFACE.md`

## ✅ Final Checklist

Before going live:

- [ ] Backend deployed and healthy
- [ ] Frontend deployed and accessible
- [ ] Database connected and migrated
- [ ] Environment variables configured
- [ ] CORS configured correctly
- [ ] Authentication working
- [ ] All features tested
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Performance acceptable
- [ ] Monitoring enabled
- [ ] Backups configured (Neon auto-backups)
- [ ] Custom domain configured (optional)

## 🎉 Success!

Your Todo App is now live!

- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-username-todo-backend.hf.space`
- **API Docs**: `https://your-username-todo-backend.hf.space/docs`

## 🤝 Support

Need help?

- **Vercel**: [vercel.com/support](https://vercel.com/support)
- **Hugging Face**: [Community Forums](https://discuss.huggingface.co)
- **Neon**: [Discord Community](https://neon.tech/discord)

---

**Built with ❤️ for the Todo Hackathon**

*Deployed on Vercel ▲ and Hugging Face 🤗*
