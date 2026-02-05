# Quickstart: Phase 4 Kubernetes Deployment

**Feature**: Phase 4 Kubernetes Deployment
**Date**: 2026-02-05
**Status**: Complete

## Prerequisites Verification

Before deploying, verify all required tools are installed:

```bash
# Check Minikube
minikube version
# Expected: minikube version: v1.32.0 or higher

# Check Helm
helm version
# Expected: version.BuildInfo{Version:"v3.x.x"}

# Check Docker
docker --version
# Expected: Docker version 24.0.0 or higher

# Check kubectl
kubectl version --client
# Expected: Client Version: v1.28.0 or higher
```

---

## Quick Deployment (Single Command)

### Step 1: Prepare Environment

```bash
# Navigate to Phase 4 directory
cd /mnt/d/todo-hackathon/phase-4-k8s-deployment

# Create .env file from example
cp .env.example .env

# Edit .env with your credentials
nano .env  # or vim, code, etc.
```

**Required Environment Variables**:
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

### Step 2: Run Deployment Script

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

**Expected Output**:
```
[INFO] Step 1: Validating prerequisites...
[SUCCESS] All required tools are installed
[INFO] Step 2: Checking Minikube status...
[SUCCESS] Minikube is already running
[INFO] Step 3: Configuring Docker to use Minikube daemon...
[SUCCESS] Docker configured to use Minikube daemon
[INFO] Step 4: Building Docker images...
[SUCCESS] Frontend image built successfully
[SUCCESS] Backend image built successfully
[INFO] Step 5: Loading environment variables from .env...
[SUCCESS] All required environment variables are set
[INFO] Step 6: Creating Kubernetes namespace...
[SUCCESS] Namespace ready
[INFO] Step 7: Deploying application with Helm...
[SUCCESS] Helm deployment completed
[INFO] Step 8: Waiting for pods to be ready (max 120 seconds)...
[SUCCESS] All pods are ready
[INFO] Step 9: Deployment complete! Access information:

==================================================
          TODO APPLICATION DEPLOYED
==================================================

🌐 Access Application:

   RECOMMENDED (WSL2/Windows):
   1. Forward Frontend Port (Keep running in a separate terminal):
      kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0

   2. Forward Backend Port (Keep running in a separate terminal):
      kubectl port-forward svc/todo-app-backend 8001:8001 -n todo-app --address 0.0.0.0

   Once forwarding is running:
   - Frontend: http://localhost:3000
   - Backend:  http://localhost:8001

   Alternative (Linux/Mac):
   Frontend: http://192.168.49.2:30300

📊 Useful Commands:
  - View pods:        kubectl get pods -n todo-app
  - View services:    kubectl get svc -n todo-app
  - Frontend logs:    kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f
  - Backend logs:     kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f
  - Scale frontend:   kubectl scale deployment -n todo-app todo-app-frontend --replicas=3

🗑️  Uninstall:
  - helm uninstall todo-app -n todo-app
  - kubectl delete namespace todo-app

==================================================
```

---

## Verification Steps

### 1. Verify Pods are Running

```bash
kubectl get pods -n todo-app
```

**Expected Output**:
```
NAME                                  READY   STATUS    RESTARTS   AGE
todo-app-backend-xxxxxxxxxx-xxxxx    1/1     Running   0          2m
todo-app-frontend-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

**Success Criteria**:
- Both pods show `1/1` in READY column
- STATUS is `Running`
- RESTARTS is `0` (or low number)

### 2. Verify Services are Exposed

```bash
kubectl get svc -n todo-app
```

**Expected Output**:
```
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
todo-app-backend      ClusterIP   10.96.xxx.xxx   <none>        8001/TCP         2m
todo-app-frontend     NodePort    10.96.xxx.xxx   <none>        3000:30300/TCP   2m
```

**Success Criteria**:
- `todo-app-frontend` is type `NodePort` with port `3000:30300`
- `todo-app-backend` is type `ClusterIP` with port `8001`

### 3. Verify Health Probes

```bash
# Check frontend health
kubectl exec -n todo-app deployment/todo-app-frontend -- curl -s http://localhost:3000/api/health

# Check backend health
kubectl exec -n todo-app deployment/todo-app-backend -- curl -s http://localhost:8001/api/health
```

**Expected Output**:
```json
{
  "status": "ok",
  "timestamp": "2026-02-05T10:30:00Z",
  "service": "frontend"
}
```

### 4. Verify Readiness Probes

```bash
# Check frontend readiness
kubectl exec -n todo-app deployment/todo-app-frontend -- curl -s http://localhost:3000/api/ready

# Check backend readiness
kubectl exec -n todo-app deployment/todo-app-backend -- curl -s http://localhost:8001/api/ready
```

**Expected Output**:
```json
{
  "status": "ready",
  "timestamp": "2026-02-05T10:30:00Z",
  "service": "backend",
  "checks": {
    "environment": "ok",
    "database": "ok"
  }
}
```

### 5. Access Frontend Application

**Option A: Port Forwarding (Recommended for WSL2/Windows)**

```bash
# Terminal 1: Forward frontend
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0

# Terminal 2: Forward backend (optional, for direct API access)
kubectl port-forward svc/todo-app-backend 8001:8001 -n todo-app --address 0.0.0.0

# Open browser
# http://localhost:3000
```

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

### 6. Test Phase 3 Features

Once the application is accessible, verify all Phase 3 features work:

**Authentication**:
1. Navigate to signup page
2. Create account with email and password
3. Sign in with credentials
4. Verify JWT token is set in cookies

**Task Management**:
1. Create a new task
2. View task in list
3. Update task title/description
4. Mark task as complete
5. Delete task

**AI Chatbot**:
1. Click chat button (bottom right)
2. Send message: "Add a task to buy groceries"
3. Verify task is created
4. Send message: "Show my tasks"
5. Verify tasks are listed
6. Send message: "Mark task 1 as complete"
7. Verify task is marked complete

---

## Troubleshooting

### Issue: Pods Not Starting

```bash
# Check pod status
kubectl get pods -n todo-app

# Describe pod for events
kubectl describe pod -n todo-app <pod-name>

# Check logs
kubectl logs -n todo-app <pod-name>
```

**Common Causes**:
- Image not found: Run `eval $(minikube docker-env)` and rebuild images
- Resource limits: Check Minikube has sufficient CPU/memory
- Missing secrets: Verify .env file has all required variables

### Issue: Health Probes Failing

```bash
# Check probe status
kubectl describe pod -n todo-app <pod-name> | grep -A 10 "Liveness\|Readiness"

# Test endpoint manually
kubectl exec -n todo-app <pod-name> -- curl -v http://localhost:3000/api/health
```

**Common Causes**:
- Backend: Database connection failed (check DATABASE_URL)
- Frontend: Missing environment variables (check BETTER_AUTH_SECRET)
- Timing: Increase initialDelaySeconds in Helm values

### Issue: Cannot Access Frontend

```bash
# Verify service is running
kubectl get svc -n todo-app

# Check if port-forward is active
ps aux | grep "kubectl port-forward"

# Try alternative access method
minikube service todo-app-frontend -n todo-app --url
```

**Common Causes**:
- Port-forward not running: Start port-forward in separate terminal
- Firewall blocking: Check Windows/Linux firewall settings
- Wrong URL: Use `minikube ip` to get correct IP address

### Issue: Backend Not Accessible from Frontend

```bash
# Check backend service DNS
kubectl exec -n todo-app deployment/todo-app-frontend -- nslookup todo-app-backend

# Test backend connectivity
kubectl exec -n todo-app deployment/todo-app-frontend -- curl -v http://todo-app-backend:8001/api/health
```

**Common Causes**:
- Service name mismatch: Verify BACKEND_URL in ConfigMap
- Port mismatch: Backend should be on port 8001
- Network policy: Check if network policies are blocking traffic

---

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

---

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

---

## Success Indicators

✅ **Deployment Successful** if:
1. All pods reach `Running` status within 120 seconds
2. Health probes return 200 OK
3. Readiness probes return 200 OK with all checks passing
4. Frontend accessible via port-forward or NodePort
5. Backend accessible from frontend pods via internal DNS
6. All Phase 3 features work without regression
7. Pods automatically restart on failure (liveness probe)
8. Unhealthy pods removed from service (readiness probe)

---

## Next Steps

After successful deployment:
1. Test horizontal pod scaling
2. Simulate pod failures and verify auto-recovery
3. Review logs for errors or warnings
4. Test with multiple concurrent users
5. Proceed to Phase 5 (Advanced Cloud Deployment)
