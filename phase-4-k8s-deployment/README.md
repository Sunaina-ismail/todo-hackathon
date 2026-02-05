# Phase 4: Kubernetes Deployment with Minikube

Deploy the Phase 3 AI-powered Todo application to a local Minikube Kubernetes cluster with production-ready infrastructure.

## Overview

This phase implements:
- **Automated Deployment**: Single-command deployment script
- **Health Monitoring**: Liveness and readiness probes for automatic recovery
- **Secure Configuration**: ConfigMaps and Secrets for environment management
- **Network Isolation**: NodePort for frontend, ClusterIP for backend
- **Horizontal Scaling**: Stateless pods that scale independently
- **AI DevOps Tools**: Integration with kubectl-ai, kagent, and Docker AI

## Prerequisites

- **Minikube** 1.32+ ([Install](https://minikube.sigs.k8s.io/docs/start/))
- **Helm** 3.x ([Install](https://helm.sh/docs/intro/install/))
- **Docker** 24+ ([Install](https://docs.docker.com/get-docker/))
- **kubectl** 1.28+ ([Install](https://kubernetes.io/docs/tasks/tools/))

Verify installations:
```bash
minikube version
helm version
docker --version
kubectl version --client
```

## Quick Start

### 1. Prepare Environment

```bash
cd phase-4-k8s-deployment

# Create .env file from example
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required Environment Variables**:
```bash
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long
OPENAI_API_KEY=sk-...  # Or another LLM provider
```

### 2. Deploy Application

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

The script will:
1. Validate prerequisites
2. Start Minikube (if not running)
3. Configure Docker to use Minikube daemon
4. Build Docker images
5. Load environment variables
6. Create Kubernetes namespace
7. Deploy with Helm
8. Wait for pods to be ready
9. Display access instructions

**Expected Time**: < 10 minutes

### 3. Access Application

**Recommended (WSL2/Windows)**:
```bash
# Terminal 1: Forward frontend
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0

# Terminal 2: Forward backend (optional)
kubectl port-forward svc/todo-app-backend 8001:8001 -n todo-app --address 0.0.0.0

# Open browser
# http://localhost:3000
```

**Alternative (Linux/Mac)**:
```bash
# Get Minikube IP
minikube ip

# Access frontend
# http://<minikube-ip>:30300
```

## Architecture

### Components

- **Frontend**: Next.js 16 with ChatKit UI (NodePort 30300)
- **Backend**: FastAPI with OpenAI Agents SDK (ClusterIP 8001)
- **Database**: External Neon PostgreSQL
- **Storage**: External Cloudflare R2 (optional)

### Health Probes

**Liveness Probe** (`/api/health`):
- Detects crashed containers
- Triggers automatic restart within 30 seconds
- Initial delay: 30s, Period: 15s

**Readiness Probe** (`/api/ready`):
- Validates environment variables (frontend)
- Tests database connectivity (backend)
- Removes unhealthy pods from service
- Initial delay: 10s, Period: 10s

### Security

- Non-root containers (UID 1000)
- Resource limits (500m CPU, 512Mi memory)
- Secrets stored in Kubernetes Secret resource
- Backend not externally accessible

## Common Operations

### View Pods
```bash
kubectl get pods -n todo-app
```

### View Logs
```bash
# Frontend logs
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend -f

# Backend logs
kubectl logs -n todo-app -l app.kubernetes.io/component=backend -f
```

### Scale Pods
```bash
# Scale frontend to 3 replicas
kubectl scale deployment -n todo-app todo-app-frontend --replicas=3

# Scale backend to 2 replicas
kubectl scale deployment -n todo-app todo-app-backend --replicas=2
```

### Update Configuration
```bash
# Edit values
nano helm/todo-app/values-dev.yaml

# Upgrade deployment
helm upgrade todo-app ./helm/todo-app -f ./helm/todo-app/values-dev.yaml -n todo-app
```

### Uninstall
```bash
# Remove Helm release
helm uninstall todo-app -n todo-app

# Delete namespace
kubectl delete namespace todo-app
```

## Verification Scripts

### Health Monitoring
```bash
./scripts/verify-health.sh
```

### Security
```bash
./scripts/verify-security.sh
```

### Network Access
```bash
./scripts/verify-network.sh
```

### Scaling
```bash
./scripts/verify-scaling.sh
```

### Phase 3 Features
```bash
./scripts/verify-phase3-features.sh
```

## AI DevOps Tools

### kubectl-ai
Natural language Kubernetes operations:
```bash
kubectl ai "show me all pods in todo-app namespace that are not ready"
```

See [kubectl-ai examples](docs/kubectl-ai-examples.md)

### kagent
Automated diagnostics and monitoring:
```bash
kagent diagnose pod-restarts --namespace todo-app
```

See [kagent guide](docs/kagent-guide.md)

### Docker AI (Gordon)
Image optimization and security scanning:
```bash
docker ai analyze frontend/Dockerfile
docker ai scan todo-backend:latest
```

See [Docker AI optimization](docs/docker-ai-optimization.md)

## Troubleshooting

### Pods Not Starting

**Check pod status**:
```bash
kubectl get pods -n todo-app
kubectl describe pod -n todo-app <pod-name>
```

**Common causes**:
- Image not found: Run `eval $(minikube docker-env)` and rebuild
- Resource limits: Check Minikube has sufficient CPU/memory
- Missing secrets: Verify .env file has all required variables

### Health Probes Failing

**Check probe status**:
```bash
kubectl describe pod -n todo-app <pod-name> | grep -A 10 "Liveness\|Readiness"
```

**Common causes**:
- Backend: Database connection failed (check DATABASE_URL)
- Frontend: Missing environment variables (check BETTER_AUTH_SECRET)
- Timing: Increase initialDelaySeconds in Helm values

### Cannot Access Frontend

**Verify service**:
```bash
kubectl get svc -n todo-app
```

**Common causes**:
- Port-forward not running: Start in separate terminal
- Firewall blocking: Check Windows/Linux firewall settings
- Wrong URL: Use `minikube ip` to get correct IP

See [troubleshooting guide](docs/troubleshooting.md) for more details.

## Documentation

- [Specification](../../specs/007-phase4-k8s-deployment/spec.md)
- [Implementation Plan](../../specs/007-phase4-k8s-deployment/plan.md)
- [Tasks](../../specs/007-phase4-k8s-deployment/tasks.md)
- [Quickstart Guide](../../specs/007-phase4-k8s-deployment/quickstart.md)

## Next Steps

After successful deployment:
1. Test horizontal pod scaling
2. Simulate pod failures and verify auto-recovery
3. Review logs for errors or warnings
4. Test with multiple concurrent users
5. Proceed to Phase 5 (Advanced Cloud Deployment)

## Support

For issues or questions:
- Check [troubleshooting guide](docs/troubleshooting.md)
- Review pod logs: `kubectl logs -n todo-app <pod-name>`
- Check pod events: `kubectl describe pod -n todo-app <pod-name>`
