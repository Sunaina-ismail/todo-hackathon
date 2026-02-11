# Phase 0 Research: Kubernetes Deployment Technologies

**Feature**: Phase 4 Kubernetes Deployment
**Date**: 2026-02-05
**Status**: Complete

## Research Questions Resolved

### 1. Minikube Docker Environment Configuration

**Decision**: Use `eval $(minikube docker-env)` to build images directly in Minikube's Docker daemon

**Rationale**:
- Eliminates need for external Docker registry
- Significantly speeds up local development cycles
- Images built within Minikube are immediately accessible to Kubernetes
- Avoids push/pull overhead for local testing

**Implementation Pattern**:
```bash
# Configure terminal to use Minikube Docker daemon
eval $(minikube docker-env)

# Build images directly in Minikube
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend

# Set imagePullPolicy to Never in Helm values
image:
  pullPolicy: Never  # Use local images only
```

**Source**: Minikube documentation - https://minikube.sigs.k8s.io/docs/handbook/pushing

**Alternatives Considered**:
- External Docker registry (rejected: adds complexity and latency)
- Host Docker daemon with registry push (rejected: slower, requires registry setup)

---

### 2. Health Probe Configuration

**Decision**: Implement HTTP-based liveness and readiness probes with different endpoints

**Rationale**:
- Liveness probes detect crashed containers and trigger automatic restarts
- Readiness probes control traffic routing to healthy pods only
- HTTP probes are simple, reliable, and provide detailed status information
- Separate endpoints allow different validation logic

**Implementation Pattern**:
```yaml
# Frontend Deployment
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 15
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /api/ready
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

# Backend Deployment
livenessProbe:
  httpGet:
    path: /api/health
    port: 8001
  initialDelaySeconds: 30
  periodSeconds: 15
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /api/ready
    port: 8001
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

**Probe Timing Strategy**:
- **initialDelaySeconds**: 30s for liveness (allow startup), 10s for readiness (faster traffic routing)
- **periodSeconds**: 15s for liveness (less frequent), 10s for readiness (more responsive)
- **failureThreshold**: 3 consecutive failures before action (prevents false positives)

**Endpoint Responsibilities**:
- `/api/health` (liveness): Basic process health check, returns 200 if process is running
- `/api/ready` (readiness): Validates environment variables (frontend) or database connectivity (backend)

**Source**: Kubernetes documentation - https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes

**Alternatives Considered**:
- TCP socket probes (rejected: less informative than HTTP)
- gRPC probes (rejected: adds complexity, HTTP sufficient for our use case)
- Exec command probes (rejected: less efficient than HTTP)

---

### 3. ConfigMaps and Secrets Management

**Decision**: Use ConfigMaps for non-sensitive configuration and Secrets for credentials

**Rationale**:
- Kubernetes-native configuration management
- Secrets are base64-encoded and can be encrypted at rest
- ConfigMaps and Secrets are injected as environment variables at runtime
- No hardcoded credentials in container images or deployment manifests
- Centralized configuration management via Helm values

**Implementation Pattern**:
```yaml
# ConfigMap for non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-app-config
data:
  BACKEND_URL: "http://todo-app-backend:8001"
  FRONTEND_URL: "http://localhost:3000"
  LLM_PROVIDER: "openai"
  LOG_LEVEL: "info"

# Secret for sensitive credentials
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
type: Opaque
data:
  DATABASE_URL: <base64-encoded>
  BETTER_AUTH_SECRET: <base64-encoded>
  OPENAI_API_KEY: <base64-encoded>

# Deployment injection
env:
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: todo-app-config
        key: LOG_LEVEL
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: todo-app-secrets
        key: DATABASE_URL
```

**Security Best Practices**:
- Secrets passed via Helm `--set` flags during deployment (not committed to Git)
- Base64 encoding applied automatically by Kubernetes
- Secrets marked as `optional: true` for non-required credentials (e.g., alternative LLM providers)
- No secrets visible in deployment logs or pod environment output

**Source**: Kubernetes documentation - https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap

**Alternatives Considered**:
- Environment variables in Dockerfile (rejected: hardcoded, insecure)
- External secret management (e.g., Vault) (rejected: overkill for local Minikube)
- ConfigMaps for secrets (rejected: not designed for sensitive data)

---

### 4. Resource Limits and Security Context

**Decision**: Set CPU/memory limits and run containers as non-root user (UID 1000)

**Rationale**:
- Resource limits prevent pods from consuming excessive cluster resources
- Memory limits trigger OOM kills if exceeded, protecting other pods
- CPU limits ensure fair resource distribution
- Non-root execution reduces security attack surface
- Dropping capabilities follows principle of least privilege

**Implementation Pattern**:
```yaml
# Deployment security context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# Container resources
resources:
  requests:
    cpu: 100m      # Minimum guaranteed CPU
    memory: 256Mi  # Minimum guaranteed memory
  limits:
    cpu: 500m      # Maximum CPU allowed
    memory: 512Mi  # Maximum memory allowed

# Container security context
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: false  # Next.js needs write access
```

**Resource Sizing Strategy**:
- **Frontend**: 100m-500m CPU, 256Mi-512Mi memory (Node.js runtime)
- **Backend**: 100m-500m CPU, 256Mi-512Mi memory (Python FastAPI)
- Requests set to 50% of limits for efficient scheduling
- Limits prevent runaway processes from affecting cluster

**Source**: Kubernetes documentation - https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace

**Alternatives Considered**:
- No resource limits (rejected: can cause cluster instability)
- Root user execution (rejected: security risk)
- Read-only root filesystem (rejected: Next.js requires write access for cache)

---

### 5. Service Types and Network Exposure

**Decision**: NodePort for frontend (port 30300), ClusterIP for backend (port 8001)

**Rationale**:
- NodePort exposes frontend externally for browser access
- ClusterIP keeps backend internal for security (no external exposure)
- Port 30300 is in NodePort range (30000-32767)
- Backend port 8001 avoids conflict with port 8000 (already in use)
- Internal DNS resolution via service names (e.g., `todo-app-backend:8001`)

**Implementation Pattern**:
```yaml
# Frontend Service (NodePort)
apiVersion: v1
kind: Service
metadata:
  name: todo-app-frontend
spec:
  type: NodePort
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30300
  selector:
    app.kubernetes.io/component: frontend

# Backend Service (ClusterIP)
apiVersion: v1
kind: Service
metadata:
  name: todo-app-backend
spec:
  type: ClusterIP
  ports:
    - port: 8001
      targetPort: 8001
  selector:
    app.kubernetes.io/component: backend
```

**Access Methods**:
- **Frontend**: `http://<minikube-ip>:30300` or `kubectl port-forward svc/todo-app-frontend 3000:3000`
- **Backend**: Internal only via `http://todo-app-backend:8001` (from frontend pods)

**Source**: Kubernetes documentation - https://kubernetes.io/docs/concepts/services-networking/service

**Alternatives Considered**:
- LoadBalancer for frontend (rejected: requires cloud provider, overkill for Minikube)
- NodePort for backend (rejected: unnecessary external exposure, security risk)
- Ingress controller (rejected: adds complexity for local development)

---

### 6. Helm Chart Structure and Values Files

**Decision**: Use standard Helm chart structure with values.yaml (production) and values-dev.yaml (Minikube)

**Rationale**:
- Helm provides templating, versioning, and rollback capabilities
- Separate values files enable environment-specific configuration
- Template helpers (_helpers.tpl) promote DRY principles
- Standard structure follows Helm best practices

**Implementation Pattern**:
```text
helm/todo-app/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Production defaults (2 replicas)
├── values-dev.yaml         # Minikube overrides (1 replica, Never pull)
├── .helmignore             # Files to exclude from package
└── templates/
    ├── _helpers.tpl        # Reusable template functions
    ├── configmap.yaml      # Non-sensitive configuration
    ├── secret.yaml         # Sensitive credentials
    ├── deployment-frontend.yaml
    ├── deployment-backend.yaml
    ├── service-frontend.yaml
    └── service-backend.yaml
```

**Template Helpers Pattern**:
```go-template
{{/* Generate common labels */}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Selector labels */}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

**Values File Strategy**:
- **values.yaml**: Production-ready defaults (2 replicas, IfNotPresent pull policy)
- **values-dev.yaml**: Minikube-specific overrides (1 replica, Never pull policy, debug logging)
- Secrets passed via `--set` flags during deployment (never committed)

**Source**: Helm documentation - https://helm.sh/docs/chart_template_guide/getting_started

**Alternatives Considered**:
- Raw Kubernetes YAML (rejected: no templating, harder to maintain)
- Kustomize (rejected: less powerful than Helm for multi-environment)
- Single values file (rejected: mixes production and development config)

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Orchestration** | Minikube | 1.32+ | Local Kubernetes cluster |
| **Package Manager** | Helm | 3.x | Chart management and deployment |
| **Container Runtime** | Docker | 24+ | Image building and execution |
| **Kubernetes** | K8s | 1.28+ | Container orchestration |
| **CLI Tool** | kubectl | 1.28+ | Cluster management |
| **Frontend** | Next.js 16 | 16.1.1 | Web application |
| **Backend** | FastAPI | Latest | API server |
| **Database** | Neon PostgreSQL | External | Data persistence |
| **Storage** | Cloudflare R2 | External | Object storage |

---

## Implementation Decisions Summary

1. **Image Building**: Use Minikube Docker daemon with `eval $(minikube docker-env)`
2. **Health Probes**: HTTP-based liveness (/api/health) and readiness (/api/ready) probes
3. **Configuration**: ConfigMaps for non-sensitive, Secrets for credentials
4. **Security**: Non-root containers (UID 1000), resource limits, dropped capabilities
5. **Networking**: NodePort (30300) for frontend, ClusterIP (8001) for backend
6. **Deployment**: Helm charts with values.yaml and values-dev.yaml
7. **Access**: kubectl port-forward for development, NodePort for testing

---

## Next Steps

- **Phase 1**: Create data-model.md with Kubernetes resource definitions
- **Phase 1**: Generate API contracts for health endpoints
- **Phase 1**: Create quickstart.md with deployment verification steps
- **Phase 2**: Generate tasks.md with actionable implementation tasks
