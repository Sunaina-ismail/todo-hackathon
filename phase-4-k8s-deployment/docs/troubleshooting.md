# Troubleshooting Guide

Common issues and solutions for Phase 4 Kubernetes deployment.

## Pods Not Starting

### Symptom
Pods stuck in `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff` state.

### Diagnosis
```bash
kubectl get pods -n todo-app
kubectl describe pod -n todo-app <pod-name>
kubectl logs -n todo-app <pod-name>
```

### Solutions

**Image Not Found**:
```bash
# Reconfigure Docker to use Minikube daemon
eval $(minikube docker-env)

# Rebuild images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend

# Verify images exist
docker images | grep todo
```

**Resource Limits**:
```bash
# Check Minikube resources
minikube status

# Increase Minikube resources
minikube stop
minikube start --cpus=4 --memory=8192
```

**Missing Secrets**:
```bash
# Verify .env file exists and has all required variables
cat .env

# Redeploy with correct secrets
./scripts/deploy.sh
```

---

## Health Probes Failing

### Symptom
Pods restarting frequently or not receiving traffic.

### Diagnosis
```bash
kubectl describe pod -n todo-app <pod-name> | grep -A 10 "Liveness\|Readiness"
kubectl logs -n todo-app <pod-name>
```

### Solutions

**Backend Database Connection**:
```bash
# Test database connectivity
kubectl exec -n todo-app deployment/todo-app-backend -- curl -v http://localhost:8001/api/ready

# Check DATABASE_URL is correct
kubectl get secret -n todo-app -o jsonpath='{.data.DATABASE_URL}' | base64 -d
```

**Frontend Environment Variables**:
```bash
# Check required env vars
kubectl exec -n todo-app deployment/todo-app-frontend -- env | grep -E "DATABASE_URL|BETTER_AUTH_SECRET"
```

**Timing Issues**:
```yaml
# Edit helm/todo-app/values-dev.yaml
healthProbes:
  backend:
    liveness:
      initialDelaySeconds: 60  # Increase from 30
    readiness:
      initialDelaySeconds: 20  # Increase from 10
```

---

## Cannot Access Frontend

### Symptom
Browser cannot connect to frontend application.

### Diagnosis
```bash
kubectl get svc -n todo-app
minikube ip
```

### Solutions

**Port-Forward Not Running**:
```bash
# Start port-forward in separate terminal
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0
```

**Firewall Blocking**:
```bash
# Windows: Allow port 3000 in Windows Firewall
# Linux: Check iptables rules
sudo iptables -L -n | grep 3000
```

**Wrong URL**:
```bash
# Get correct Minikube IP
MINIKUBE_IP=$(minikube ip)
echo "Frontend: http://$MINIKUBE_IP:30300"
```

**Service Not Ready**:
```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# If no endpoints, check pod readiness
kubectl get pods -n todo-app
```

---

## Backend Not Accessible from Frontend

### Symptom
Frontend cannot communicate with backend API.

### Diagnosis
```bash
# Test internal DNS resolution
kubectl exec -n todo-app deployment/todo-app-frontend -- nslookup todo-app-backend

# Test backend connectivity
kubectl exec -n todo-app deployment/todo-app-frontend -- curl -v http://todo-app-backend:8001/api/health
```

### Solutions

**Service Name Mismatch**:
```bash
# Verify backend service name
kubectl get svc -n todo-app

# Check ConfigMap has correct BACKEND_URL
kubectl get configmap -n todo-app -o yaml | grep BACKEND_URL
```

**Port Mismatch**:
```bash
# Backend should be on port 8001
kubectl get svc todo-app-backend -n todo-app -o jsonpath='{.spec.ports[0].port}'
```

**Network Policy Blocking**:
```bash
# Check for network policies
kubectl get networkpolicies -n todo-app
```

---

## Helm Deployment Fails

### Symptom
`helm upgrade --install` command fails with validation errors.

### Diagnosis
```bash
# Validate Helm chart
helm lint ./helm/todo-app

# Test template rendering
helm template todo-app ./helm/todo-app -f ./helm/todo-app/values-dev.yaml
```

### Solutions

**Template Syntax Error**:
```bash
# Check for YAML syntax errors
helm template todo-app ./helm/todo-app -f ./helm/todo-app/values-dev.yaml --debug
```

**Missing Values**:
```bash
# Verify all required values are set
cat helm/todo-app/values-dev.yaml
```

**Namespace Issues**:
```bash
# Ensure namespace exists
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
```

---

## Secrets Exposed in Logs

### Symptom
Sensitive information visible in pod logs or environment output.

### Diagnosis
```bash
# Check logs for secrets
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app --tail=100 | grep -iE "(DATABASE_URL|API_KEY|SECRET)"

# Check pod environment
kubectl exec -n todo-app deployment/todo-app-backend -- env
```

### Solutions

**Remove Secrets from Logs**:
- Update application code to not log sensitive values
- Use structured logging with secret redaction

**Verify Secret Storage**:
```bash
# Secrets should be base64-encoded
kubectl get secret -n todo-app -o yaml
```

**Check Git History**:
```bash
# Ensure .env not committed
git log --all --full-history --source -- .env
```

---

## Minikube Issues

### Symptom
Minikube fails to start or becomes unresponsive.

### Diagnosis
```bash
minikube status
minikube logs
```

### Solutions

**Restart Minikube**:
```bash
minikube stop
minikube start
```

**Delete and Recreate**:
```bash
minikube delete
minikube start --cpus=4 --memory=8192
```

**Check Docker Driver**:
```bash
# Ensure Docker is running
docker ps

# Start Minikube with Docker driver
minikube start --driver=docker
```

---

## WSL2 Networking Issues

### Symptom
Cannot access Minikube services from Windows browser.

### Solutions

**Use Port-Forward**:
```bash
# Forward with --address 0.0.0.0 to allow Windows access
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0
```

**Check WSL2 Firewall**:
```bash
# Allow port in Windows Firewall
# Settings > Network & Internet > Windows Firewall > Advanced settings
```

**Use WSL2 IP**:
```bash
# Get WSL2 IP
ip addr show eth0 | grep inet

# Access via WSL2 IP
# http://<wsl2-ip>:3000
```

---

## Getting Help

If issues persist:

1. **Collect Diagnostics**:
```bash
kubectl get all -n todo-app
kubectl describe pods -n todo-app
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app --tail=100
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

2. **Check Documentation**:
- [Kubernetes Troubleshooting](https://kubernetes.io/docs/tasks/debug/)
- [Minikube Troubleshooting](https://minikube.sigs.k8s.io/docs/handbook/troubleshooting/)
- [Helm Troubleshooting](https://helm.sh/docs/faq/troubleshooting/)

3. **Use AI DevOps Tools**:
```bash
kubectl ai "diagnose issues in todo-app namespace"
kagent diagnose --namespace todo-app
```
