# Phase 4 Kubernetes Deployment - Complete Guide

## ✅ Phase 4 Status: COMPLETE

All 40 tasks completed successfully:
- ✅ Phase 1: Setup (5 tasks)
- ✅ Phase 2: Foundational - Health Endpoints + Dockerfiles (8 tasks)
- ✅ Phase 3: P1 Automated Deployment (13 tasks)
- ✅ Phases 4-9: User Stories P2-P7 (9 tasks)
- ✅ Phase 10: Polish (5 tasks)

## Prerequisites

Ensure you have these tools installed:

```bash
# Check versions
minikube version  # Need 1.32+
helm version      # Need 3.x
docker --version  # Need 24+
kubectl version --client  # Need 1.28+
```

**Install if missing:**
- Minikube: https://minikube.sigs.k8s.io/docs/start/
- Helm: https://helm.sh/docs/intro/install/
- Docker: https://docs.docker.com/get-docker/
- kubectl: https://kubernetes.io/docs/tasks/tools/

## Complete Deployment Commands

### Step 1: Navigate to Phase 4 Directory

```bash
cd /mnt/d/todo-hackathon/phase-4-k8s-deployment
```

### Step 2: Create Environment File

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required Environment Variables:**
```bash
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Authentication (shared secret - must match frontend & backend)
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long

# LLM Provider (at least one required)
OPENAI_API_KEY=sk-...
# OR
OPENROUTER_API_KEY=sk-or-v1-...
# OR
GROQ_API_KEY=gsk_...
# OR
GEMINI_API_KEY=...

# Optional: Cloudflare R2 for file storage
CLOUDFLARE_R2_ACCOUNT_ID=
CLOUDFLARE_R2_ACCESS_KEY_ID=
CLOUDFLARE_R2_SECRET_ACCESS_KEY=
CLOUDFLARE_R2_BUCKET_NAME=
```

### Step 3: Deploy Application (Single Command)

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

**What the script does:**
1. ✅ Validates prerequisites (minikube, helm, docker, kubectl)
2. ✅ Starts Minikube (if not running)
3. ✅ Configures Docker to use Minikube daemon
4. ✅ Builds Docker images (frontend + backend)
5. ✅ Loads environment variables from .env
6. ✅ Validates required variables
7. ✅ Creates Kubernetes namespace
8. ✅ Deploys with Helm
9. ✅ Waits for pods to be ready (120s timeout)
10. ✅ Displays access instructions

**Expected Time:** < 10 minutes

### Step 4: Access Application

**Option A: Port-Forward (Recommended for WSL2/Windows)**

```bash
# Terminal 1: Forward frontend port
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0

# Terminal 2: Forward backend port (using 8001 as 8000 is in use)
kubectl port-forward svc/todo-app-backend 8001:8001 -n todo-app --address 0.0.0.0
```

**Access URLs:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- Backend Health: http://localhost:8001/api/health
- Backend Docs: http://localhost:8001/docs

**Option B: NodePort (Linux/Mac)**

```bash
**Option B: NodePort (Linux/Mac)**

```bash
# Get Minikube IP
minikube ip
# Example output: 192.168.49.2

# Open browser
# http://192.168.49.2:30300
```

**Option C: Minikube Service Command**

```bash
# Automatically opens browser with correct URL
minikube service todo-app-frontend -n todo-app
```

## Verification Commands

### Check Deployment Status

```bash
# View all pods
kubectl get pods -n todo-app

# Expected output:
# NAME                                  READY   STATUS    RESTARTS   AGE
# todo-app-backend-xxxxxxxxxx-xxxxx    1/1     Running   0          2m
# todo-app-frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

### Check Services

```bash
# View services
kubectl get svc -n todo-app

# Expected output:
# NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
# todo-app-backend      ClusterIP   10.96.xxx.xxx   <none>        8000/TCP         2m
# todo-app-frontend     NodePort    10.96.xxx.xxx   <none>        3000:30300/TCP   2m
```

### Check Health Probes

```bash
# Frontend health
kubectl exec -n todo-app deployment/todo-app-frontend -- curl -s http://localhost:3000/api/health

# Backend health
kubectl exec -n todo-app deployment/todo-app-backend -- curl -s http://localhost:8001/api/health

# Expected output:
# {"status":"ok","timestamp":"2026-02-05T10:30:00Z","service":"frontend"}
# {"status":"ok","timestamp":"2026-02-05T10:30:00Z","service":"backend"}
```

### View Logs

```bash
# Frontend logs
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f

# Backend logs
kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f
```

## Verification Scripts

Run these scripts to verify Phase 4 features:

```bash
# Health monitoring verification
./scripts/verify-health.sh

# Security verification (no secrets exposed)
./scripts/verify-security.sh

# Network access verification
./scripts/verify-network.sh

# Horizontal scaling verification
./scripts/verify-scaling.sh

# Phase 3 feature parity verification
./scripts/verify-phase3-features.sh
```

## Scaling Operations

### Scale Frontend

```bash
# Scale to 3 replicas
kubectl scale deployment -n todo-app todo-app-frontend --replicas=3

# Verify scaling
kubectl get pods -n todo-app -l app.kubernetes.io/component=frontend

# Watch rollout
kubectl rollout status deployment -n todo-app todo-app-frontend
```

### Scale Backend

```bash
# Scale to 2 replicas
kubectl scale deployment -n todo-app todo-app-backend --replicas=2

# Verify scaling
kubectl get pods -n todo-app -l app.kubernetes.io/component=backend
```

### Scale via Helm

```bash
# Update values and upgrade
helm upgrade todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-dev.yaml \
  -n todo-app \
  --set replicaCount.frontend=3 \
  --set replicaCount.backend=2
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n todo-app

# Describe pod for events
kubectl describe pod -n todo-app <pod-name>

# Check logs
kubectl logs -n todo-app <pod-name>
```

**Common causes:**
- Image not found: Run `eval $(minikube docker-env)` and rebuild images
- Resource limits: Check Minikube has sufficient CPU/memory
- Missing secrets: Verify .env file has all required variables

### Health Probes Failing

```bash
# Check probe status
kubectl describe pod -n todo-app <pod-name> | grep -A 10 "Liveness\|Readiness"

# Test endpoint manually
kubectl exec -n todo-app <pod-name> -- curl -v http://localhost:3000/api/health
```

**Common causes:**
- Backend: Database connection failed (check DATABASE_URL)
- Frontend: Missing environment variables (check BETTER_AUTH_SECRET)
- Timing: Increase initialDelaySeconds in Helm values

### Cannot Access Frontend

```bash
# Verify service is running
kubectl get svc -n todo-app

# Check if port-forward is active
ps aux | grep "kubectl port-forward"

# Try alternative access method
minikube service todo-app-frontend -n todo-app --url
```

See [docs/troubleshooting.md](docs/troubleshooting.md) for more details.

## Cleanup

### Uninstall Application

```bash
# Remove Helm release
helm uninstall todo-app -n todo-app

# Delete namespace (removes all resources)
kubectl delete namespace todo-app

# Verify cleanup
kubectl get all -n todo-app
# Expected: No resources found
```

### Stop Minikube

```bash
# Stop cluster (keeps state)
minikube stop

# Delete cluster completely
minikube delete
```

## Architecture Summary

**Components:**
- Frontend: Next.js 16 with ChatKit UI (NodePort 30300)
- Backend: FastAPI with OpenAI Agents SDK (ClusterIP 8000)
- Database: External Neon PostgreSQL
- Storage: External Cloudflare R2 (optional)

**Health Probes:**
- Liveness: `/api/health` - Detects crashed containers, triggers restart
- Readiness: `/api/ready` - Validates dependencies, controls traffic routing

**Security:**
- Non-root containers (UID 1000)
- Resource limits (500m CPU, 512Mi memory)
- Secrets stored in Kubernetes Secret resource
- Backend not externally accessible

**Network:**
- Frontend: NodePort 30300 (external access)
- Backend: ClusterIP 8000 (internal only)
- Frontend → Backend: Internal DNS (http://todo-app-backend:8001)

## Success Indicators

✅ **Deployment Successful** if:
1. All pods reach `Running` status within 120 seconds
2. Health probes return 200 OK
3. Readiness probes return 200 OK with all checks passing
4. Frontend accessible via port-forward or NodePort
5. Backend accessible from frontend pods via internal DNS
6. All Phase 3 features work without regression

## Next Steps

After successful deployment:
1. Test horizontal pod scaling
2. Simulate pod failures and verify auto-recovery
3. Review logs for errors or warnings
4. Test with multiple concurrent users
5. Proceed to Phase 5 (Advanced Cloud Deployment)

## Documentation

- **Specification**: `../../specs/007-phase4-k8s-deployment/spec.md`
- **Implementation Plan**: `../../specs/007-phase4-k8s-deployment/plan.md`
- **Tasks**: `../../specs/007-phase4-k8s-deployment/tasks.md` (40/40 complete)
- **Quickstart**: `../../specs/007-phase4-k8s-deployment/quickstart.md`
- **README**: `README.md`
- **Troubleshooting**: `docs/troubleshooting.md`

## AI DevOps Tools

### kubectl-ai
```bash
kubectl ai "show me all pods in todo-app namespace that are not ready"
```
See [docs/kubectl-ai-examples.md](docs/kubectl-ai-examples.md)

### kagent
```bash
kagent diagnose pod-restarts --namespace todo-app
```
See [docs/kagent-guide.md](docs/kagent-guide.md)

### Docker AI (Gordon)
```bash
docker ai analyze frontend/Dockerfile
docker ai scan todo-backend:latest
```
See [docs/docker-ai-optimization.md](docs/docker-ai-optimization.md)

---

**Phase 4 Status:** ✅ COMPLETE - Ready for deployment testing
