# 🚀 Pre-Deployment Checklist

## ✅ Backend Deployment to Hugging Face Spaces

### Step 1: Verify Backend Files

**Required files to upload to Hugging Face:**
```
backend/
├── Dockerfile ✓ (Port 7860 configured)
├── pyproject.toml
├── uv.lock
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

### Step 2: Create Neon Database

1. Go to https://console.neon.tech
2. Click "Create Project"
3. Name: `todo-app-production`
4. Region: Choose closest to your users
5. Copy connection string (looks like):
   ```
   postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
6. **IMPORTANT**: Keep this connection string safe!

### Step 3: Generate Secrets

```bash
# Generate BETTER_AUTH_SECRET (32+ characters)
openssl rand -base64 32

# Example output:
# dZLDHNC3q5cucIRX1qXkXAMg+y9z8b9IPbI27HnHJosqRgOJrhxby5eUedaltzR7

# Save this - you'll need it for BOTH backend and frontend!
```

### Step 4: Create Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Configure:
   - **Owner**: Your username
   - **Space name**: `todo-backend` (or your choice)
   - **License**: MIT
   - **SDK**: Docker ⚠️ IMPORTANT
   - **Hardware**: CPU basic (free)
   - **Visibility**: Public or Private

### Step 5: Configure Hugging Face Secrets

In your Space → Settings → Variables and secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `DATABASE_URL` | Your Neon connection string | `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require` |
| `BETTER_AUTH_SECRET` | Generated secret from Step 3 | `dZLDHNC3q5cucIRX1qXkXAMg+y9z8b9IPbI27HnHJosqRgOJrhxby5eUedaltzR7` |
| `ALLOWED_ORIGINS` | Your Vercel frontend URL | `https://todo-app.vercel.app` |
| `PORT` | 7860 | `7860` |
| `ENVIRONMENT` | production | `production` |
| `JWT_ALGORITHM` | HS256 | `HS256` |

**⚠️ CRITICAL**:
- `BETTER_AUTH_SECRET` must be EXACTLY the same for backend and frontend
- `ALLOWED_ORIGINS` must include your Vercel URL (you'll add this after frontend deployment)

### Step 6: Upload Backend Files

**Option A: Git (Recommended)**
```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR-USERNAME/todo-backend
cd todo-backend

# Copy backend files
cp -r /path/to/phase-2-todo-full-stack/backend/* .

# Commit and push
git add .
git commit -m "Initial backend deployment"
git push
```

**Option B: Web UI**
1. Go to your Space → Files
2. Click "Add file" → "Upload files"
3. Drag and drop all backend files
4. Commit changes

### Step 7: Monitor Deployment

1. Go to your Space → Logs tab
2. Watch the build process (takes 3-5 minutes)
3. Look for: `Application startup complete`
4. Your backend will be at: `https://YOUR-USERNAME-todo-backend.hf.space`

### Step 8: Test Backend

```bash
# Health check
curl https://YOUR-USERNAME-todo-backend.hf.space/health

# Should return: {"status":"healthy"}

# API documentation
# Visit: https://YOUR-USERNAME-todo-backend.hf.space/docs
```

---

## ✅ Frontend Deployment to Vercel

### Step 1: Prepare Frontend

**Verify Next.js configuration:**
```typescript
// next.config.ts should have:
output: 'standalone', ✓ (Already configured)
```

### Step 2: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 3: Deploy Frontend

```bash
# Navigate to frontend directory
cd /mnt/d/todo-hackathon/phase-2-todo-full-stack/frontend

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? todo-app (or your choice)
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

### Step 4: Configure Vercel Environment Variables

In Vercel Dashboard → Your Project → Settings → Environment Variables:

| Variable Name | Value | Environment |
|---------------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://YOUR-USERNAME-todo-backend.hf.space` | Production |
| `DATABASE_URL` | Same Neon connection string as backend | Production |
| `BETTER_AUTH_SECRET` | Same secret as backend | Production |
| `BETTER_AUTH_URL` | `https://your-app.vercel.app` | Production |
| `NEXT_PUBLIC_APP_URL` | `https://your-app.vercel.app` | Production |

**⚠️ CRITICAL**:
- `BETTER_AUTH_SECRET` must match backend EXACTLY
- `NEXT_PUBLIC_API_URL` must be your Hugging Face backend URL
- `DATABASE_URL` must be the same Neon database

### Step 5: Update Backend CORS

After frontend is deployed, update Hugging Face backend:

1. Go to Hugging Face Space → Settings → Variables and secrets
2. Update `ALLOWED_ORIGINS`:
   ```
   https://your-app.vercel.app,https://your-app-git-main.vercel.app
   ```
3. Include both production and preview URLs

### Step 6: Redeploy Frontend

```bash
# After setting environment variables, redeploy
vercel --prod
```

### Step 7: Test Frontend

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Click "Sign Up"
3. Create an account
4. Verify you can:
   - See the dashboard with analytics
   - Create tasks
   - Edit tasks
   - Delete tasks
   - Filter and search tasks

---

## 🔍 Final Verification Checklist

### Backend (Hugging Face)
- [ ] Space created with Docker SDK
- [ ] All backend files uploaded
- [ ] All secrets configured correctly
- [ ] Build completed successfully
- [ ] Health check returns `{"status":"healthy"}`
- [ ] API docs accessible at `/docs`
- [ ] Database migrations ran successfully

### Frontend (Vercel)
- [ ] Project deployed successfully
- [ ] All environment variables set
- [ ] Build completed without errors
- [ ] Site is accessible
- [ ] Can sign up and create account
- [ ] Can sign in
- [ ] Dashboard loads with analytics
- [ ] Can create, edit, delete tasks
- [ ] Filters and search work

### Integration
- [ ] Frontend can communicate with backend
- [ ] No CORS errors in browser console
- [ ] Authentication works (JWT tokens)
- [ ] Tasks are saved to database
- [ ] User isolation works (can only see own tasks)

---

## 🐛 Common Issues and Solutions

### Issue 1: CORS Error

**Error**: `Access to fetch at 'https://backend.hf.space' from origin 'https://app.vercel.app' has been blocked by CORS`

**Solution**:
1. Go to Hugging Face Space → Settings → Secrets
2. Update `ALLOWED_ORIGINS` to include your Vercel URL:
   ```
   https://your-app.vercel.app,https://your-app-git-main.vercel.app
   ```
3. Wait for Space to rebuild (automatic)

### Issue 2: JWT Verification Failed

**Error**: `Invalid token` or `Unauthorized`

**Solution**:
1. Verify `BETTER_AUTH_SECRET` is EXACTLY the same in both:
   - Hugging Face backend secrets
   - Vercel frontend environment variables
2. No extra spaces or characters
3. Redeploy both if you change it

### Issue 3: Database Connection Error

**Error**: `connection refused` or `SSL required`

**Solution**:
1. Verify `DATABASE_URL` format:
   ```
   postgresql://user:pass@host:5432/db?sslmode=require
   ```
2. Ensure `?sslmode=require` is at the end
3. Check Neon database is active (not paused)
4. Verify connection string is correct

### Issue 4: Hugging Face Build Fails

**Error**: Build fails during Docker build

**Solution**:
1. Check Logs tab for specific error
2. Verify all files are uploaded
3. Ensure `pyproject.toml` and `uv.lock` are present
4. Check Python version is 3.13+

### Issue 5: Vercel Build Fails

**Error**: Build fails during Next.js build

**Solution**:
1. Check build logs in Vercel dashboard
2. Verify all environment variables are set
3. Ensure `DATABASE_URL` is set (required for Better Auth)
4. Check for TypeScript errors

---

## 📝 Deployment URLs

After successful deployment, save these URLs:

```
Backend API: https://YOUR-USERNAME-todo-backend.hf.space
Backend Docs: https://YOUR-USERNAME-todo-backend.hf.space/docs
Frontend: https://your-app.vercel.app
```

---

## 🎉 Success Criteria

Your deployment is successful when:

1. ✅ Backend health check returns `{"status":"healthy"}`
2. ✅ Frontend loads without errors
3. ✅ You can sign up and create an account
4. ✅ You can sign in with your credentials
5. ✅ Dashboard shows analytics (even if all zeros)
6. ✅ You can create a task
7. ✅ Task appears in the list
8. ✅ You can edit the task
9. ✅ You can delete the task
10. ✅ No CORS errors in browser console

---

## 🚀 Ready to Deploy!

Your project is now **100% ready** for deployment with:

✅ Backend Dockerfile configured for Hugging Face (port 7860)
✅ Frontend configured for Vercel (standalone output)
✅ All environment variables documented
✅ Comprehensive deployment guides
✅ Troubleshooting solutions
✅ Testing checklist

**Next Steps:**
1. Follow "Backend Deployment to Hugging Face Spaces" section
2. Then follow "Frontend Deployment to Vercel" section
3. Test everything using the verification checklist
4. Celebrate! 🎉

Good luck with your deployment! 🚀
