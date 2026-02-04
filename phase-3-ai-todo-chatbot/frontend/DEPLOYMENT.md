# 🚀 Todo App Frontend - Vercel Deployment Guide

## ✅ Build Status

**Frontend build completed successfully with 0 errors!**

```
✓ Compiled successfully in 92s
✓ Generating static pages (9/9) in 2.6s
✓ All routes generated successfully
```

## 📋 Pre-Deployment Checklist

### 1. Backend Deployment (Do This First!)

Before deploying the frontend, deploy your backend to Hugging Face:

- [ ] Backend deployed to Hugging Face Spaces
- [ ] Backend URL obtained (e.g., `https://username-todo-app-backend.hf.space`)
- [ ] Backend health check working (`/health` endpoint)
- [ ] Neon PostgreSQL database configured
- [ ] `BETTER_AUTH_SECRET` generated and saved

**Backend Deployment Guide**: See `backend/README_HUGGINGFACE.md`

### 2. Environment Variables

You'll need these values for Vercel:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Your Hugging Face backend URL | `https://username-todo-backend.hf.space` |
| `BETTER_AUTH_SECRET` | **MUST match backend secret** | `dZLDHNC3q5cucIRX1qXkXAMg+y9z8b9IPbI27HnHJos=` |
| `BETTER_AUTH_URL` | Your Vercel frontend URL | `https://todo-app.vercel.app` |
| `DATABASE_URL` | Same Neon database as backend | `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require` |

**Critical**: `BETTER_AUTH_SECRET` must be **exactly the same** on both frontend and backend!

## 🌐 Deploying to Vercel

### Method 1: Deploy via Vercel Dashboard (Recommended)

#### Step 1: Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "feat: ready for deployment"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR-USERNAME/todo-app.git
git branch -M main
git push -u origin main
```

#### Step 2: Import to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Click **"Import Project"**
3. Select your GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `phase-3-ai-todo-chatbot/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

#### Step 3: Configure Environment Variables

In Vercel project settings → **Environment Variables**, add:

```bash
# Backend API URL (from Hugging Face)
NEXT_PUBLIC_API_URL=https://YOUR-USERNAME-todo-backend.hf.space

# Authentication Secret (MUST match backend!)
BETTER_AUTH_SECRET=your_32_char_secret_from_backend

# Frontend URL (will be provided by Vercel)
BETTER_AUTH_URL=https://your-project.vercel.app

# Database URL (same as backend)
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
```

**Important Notes**:
- Add variables for **Production**, **Preview**, and **Development** environments
- For `BETTER_AUTH_URL`, use your actual Vercel URL after first deployment
- No trailing slashes in URLs

#### Step 4: Deploy

1. Click **"Deploy"**
2. Vercel will:
   - Install dependencies
   - Run build
   - Deploy to production
3. Build takes ~2-3 minutes
4. You'll get a URL like: `https://your-project.vercel.app`

#### Step 5: Update Backend CORS

After deployment, update your Hugging Face backend:

1. Go to your Space → **Settings** → **Variables and secrets**
2. Update `ALLOWED_ORIGINS`:
   ```
   https://your-project.vercel.app,https://your-project-git-main.vercel.app
   ```
3. Include both production and preview URLs

#### Step 6: Update BETTER_AUTH_URL

1. Go back to Vercel → **Settings** → **Environment Variables**
2. Update `BETTER_AUTH_URL` with your actual Vercel URL
3. Redeploy to apply changes

### Method 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd phase-3-ai-todo-chatbot/frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? todo-app-frontend
# - Directory? ./
# - Override settings? No

# Add environment variables
vercel env add NEXT_PUBLIC_API_URL
vercel env add BETTER_AUTH_SECRET
vercel env add BETTER_AUTH_URL
vercel env add DATABASE_URL

# Deploy to production
vercel --prod
```

## 🧪 Testing Your Deployment

### 1. Health Check

Visit your deployed frontend:
```
https://your-project.vercel.app
```

Expected: Landing page loads correctly

### 2. Authentication Test

1. Click **"Sign Up"**
2. Create a test account
3. Verify you're redirected to dashboard
4. Check browser console for errors

### 3. Dashboard Test

1. Dashboard should load with all 6 stat cards
2. All 4 charts should render
3. No loading delays or errors

### 4. Tasks Test

1. Navigate to **Tasks** page
2. Create a new task
3. Test sorting (Date Created, Priority, etc.)
4. Test filtering (Status, Priority)
5. Test search functionality

### 5. API Connection Test

Open browser console and check:
```javascript
// Should see successful API calls
fetch('https://your-backend.hf.space/health')
  .then(r => r.json())
  .then(console.log)
```

## 🐛 Troubleshooting

### Build Fails on Vercel

**Problem**: Build fails with TypeScript errors

**Solutions**:
- Run `npm run build` locally first
- Fix any TypeScript errors
- Commit and push changes
- Redeploy

### CORS Errors

**Problem**: `Access-Control-Allow-Origin` errors in console

**Solutions**:
- Verify `ALLOWED_ORIGINS` in backend includes your Vercel URL
- Include both production and preview URLs
- No trailing slashes
- Format: `https://domain1.com,https://domain2.com`

### Authentication Fails

**Problem**: Can't sign in or sign up

**Solutions**:
- Verify `BETTER_AUTH_SECRET` matches backend **exactly**
- Check `BETTER_AUTH_URL` is your actual Vercel URL
- Verify `DATABASE_URL` is correct
- Check backend logs for JWT errors

### API Calls Fail

**Problem**: Dashboard shows no data or errors

**Solutions**:
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running (visit `/health` endpoint)
- Verify backend CORS allows your frontend URL
- Check browser console for specific errors

### Environment Variables Not Working

**Problem**: Variables are undefined

**Solutions**:
- Ensure variables start with `NEXT_PUBLIC_` for client-side access
- Redeploy after adding/changing variables
- Check variables are set for correct environment (Production/Preview)
- Clear browser cache

### Slow First Load

**Problem**: First page load is slow

**Solutions**:
- Hugging Face free tier sleeps after inactivity
- First request wakes up backend (~10-15 seconds)
- Subsequent requests are fast
- Consider upgrading to persistent hardware

## 🔄 Updating Your Deployment

### Automatic Deployments

Vercel automatically deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "feat: add new feature"
git push

# Vercel automatically:
# 1. Detects push
# 2. Runs build
# 3. Deploys to preview URL
# 4. Deploys to production (if main branch)
```

### Manual Deployments

```bash
# Deploy from CLI
cd phase-3-ai-todo-chatbot/frontend
vercel --prod
```

### Rollback

If deployment has issues:

1. Go to Vercel Dashboard → **Deployments**
2. Find previous working deployment
3. Click **"..."** → **"Promote to Production"**

## 📊 Monitoring

Vercel provides:

- **Analytics**: Page views, performance metrics
- **Logs**: Real-time function logs
- **Speed Insights**: Core Web Vitals
- **Deployment History**: All deployments with status

Access: Vercel Dashboard → Your Project → **Analytics/Logs**

## 🔐 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use Vercel's encrypted secrets
   - Rotate secrets regularly

2. **API Security**
   - Always use HTTPS
   - Validate JWT tokens
   - Implement rate limiting

3. **Database Security**
   - Use SSL connections (`?sslmode=require`)
   - Strong passwords
   - Regular backups

4. **CORS Configuration**
   - Only allow trusted domains
   - No wildcards in production

## 💰 Costs

- **Vercel Hobby (Free)**:
  - 100GB bandwidth/month
  - Unlimited deployments
  - Automatic HTTPS
  - Perfect for personal projects

- **Vercel Pro ($20/month)**:
  - 1TB bandwidth
  - Team collaboration
  - Advanced analytics
  - Password protection

## 🌟 Features Enabled

Your deployed app includes:

- ✅ Server-side rendering (SSR)
- ✅ Static generation where possible
- ✅ Automatic code splitting
- ✅ Image optimization
- ✅ Edge caching
- ✅ Automatic HTTPS
- ✅ Custom domains support
- ✅ Preview deployments for PRs

## 📖 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Environment Variables Guide](https://vercel.com/docs/concepts/projects/environment-variables)
- [Custom Domains](https://vercel.com/docs/concepts/projects/domains)

## 🎯 Post-Deployment Checklist

After successful deployment:

- [ ] Frontend accessible at Vercel URL
- [ ] Backend accessible at Hugging Face URL
- [ ] Sign up/Sign in works
- [ ] Dashboard loads with data
- [ ] Tasks CRUD operations work
- [ ] Sorting and filtering work
- [ ] Search functionality works
- [ ] No console errors
- [ ] Mobile responsive
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] Custom domain configured (optional)

## 🤝 Support

- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Community**: [Vercel Discord](https://vercel.com/discord)
- **Documentation**: [vercel.com/docs](https://vercel.com/docs)

---

**Built with ❤️ for the Todo Hackathon**

*Deployed on Vercel ▲*
