# kubectl-ai Examples for Todo Application

This document provides working examples of using kubectl-ai for managing the Todo application Kubernetes deployment.

## Prerequisites

Install kubectl-ai:
```bash
# Installation instructions
kubectl krew install ai
```

## Example 1: Show Pods Not Ready

**Command**:
```bash
kubectl ai "show me all pods in todo-app namespace that are not ready"
```

**Expected Output**:
```bash
# kubectl-ai will generate and execute:
kubectl get pods -n todo-app --field-selector=status.phase!=Running

# Or if all pods are ready:
No resources found in todo-app namespace.
```

**Explanation**: kubectl-ai translates natural language into the appropriate kubectl command to filter pods by readiness status.

---

## Example 2: Describe Deployment with Health Probes

**Command**:
```bash
kubectl ai "describe the frontend deployment and explain the health probes"
```

**Expected Output**:
```bash
# kubectl-ai will generate and execute:
kubectl describe deployment todo-app-frontend -n todo-app

# Output includes:
# Liveness:  http-get http://:http/api/health delay=30s timeout=5s period=15s
# Readiness: http-get http://:http/api/ready delay=10s timeout=5s period=10s
```

**Explanation**: kubectl-ai describes the deployment and highlights the configured liveness and readiness probes with their timing parameters.

---

## Example 3: Show Recent Backend Logs

**Command**:
```bash
kubectl ai "show me the logs from the backend pod for the last 5 minutes"
```

**Expected Output**:
```bash
# kubectl-ai will generate and execute:
kubectl logs -n todo-app -l app.kubernetes.io/component=backend --since=5m

# Sample output:
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Explanation**: kubectl-ai translates the time-based log request into the appropriate kubectl logs command with the --since flag.

---

## Additional Useful Commands

### Check Resource Usage
```bash
kubectl ai "show me CPU and memory usage for all pods in todo-app namespace"
```

### Find Failed Pods
```bash
kubectl ai "find any pods that have restarted more than once in todo-app namespace"
```

### Check Service Endpoints
```bash
kubectl ai "show me all service endpoints in todo-app namespace"
```

---

## Tips for Using kubectl-ai

1. **Be specific**: Include namespace, resource type, and specific criteria
2. **Use natural language**: kubectl-ai understands conversational queries
3. **Verify commands**: kubectl-ai shows the generated command before execution
4. **Combine with grep**: You can pipe kubectl-ai output to grep for further filtering

---

## Troubleshooting

If kubectl-ai doesn't understand your query:
1. Simplify the request
2. Use more specific Kubernetes terminology
3. Break complex queries into multiple simpler ones
4. Check kubectl-ai documentation: `kubectl ai --help`
