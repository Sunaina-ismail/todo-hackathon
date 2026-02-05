# Data Model: Kubernetes Resources

**Feature**: Phase 4 Kubernetes Deployment
**Date**: 2026-02-05
**Status**: Complete

## Overview

This document defines all Kubernetes resources required for deploying the Phase 3 Todo application to Minikube. Each resource is treated as an entity with specific fields, relationships, and validation rules.

---

## Resource Entities

### 1. Frontend Deployment

**Entity Name**: `todo-app-frontend` (Deployment)

**Purpose**: Manages frontend pod replicas running Next.js 16 application with ChatKit UI

**Fields**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-app-frontend
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: frontend
    app.kubernetes.io/instance: todo-app
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1  # Configurable via values.yaml
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-app
      app.kubernetes.io/component: frontend
  template:
    metadata:
      labels:
        app.kubernetes.io/name: todo-app
        app.kubernetes.io/component: frontend
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: Never  # Use local Minikube images
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 15
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        envFrom:
        - configMapRef:
            name: todo-app-config
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: DATABASE_URL
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: BETTER_AUTH_SECRET
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: false
```

**Validation Rules**:
- `replicas` must be >= 1
- `image` must exist in Minikube Docker daemon
- `imagePullPolicy` must be "Never" for local development
- `containerPort` must be 3000 (Next.js default)
- Resource requests must be <= limits
- Security context must enforce non-root execution

**Relationships**:
- References: `todo-app-config` ConfigMap, `todo-app-secrets` Secret
- Managed by: `todo-app-frontend` Service
- Exposes: Port 3000 for HTTP traffic

**State Transitions**:
1. **Pending** → Waiting for image pull and resource allocation
2. **Running** → Container started, health probes executing
3. **Ready** → Readiness probe passed, receiving traffic
4. **Failed** → Liveness probe failed, container restarting

---

### 2. Backend Deployment

**Entity Name**: `todo-app-backend` (Deployment)

**Purpose**: Manages backend pod replicas running FastAPI with OpenAI Agents SDK and MCP tools

**Fields**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-app-backend
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: backend
    app.kubernetes.io/instance: todo-app
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1  # Configurable via values.yaml
  selector:
    matchLabels:
      app.kubernetes.io/name: todo-app
      app.kubernetes.io/component: backend
  template:
    metadata:
      labels:
        app.kubernetes.io/name: todo-app
        app.kubernetes.io/component: backend
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: Never  # Use local Minikube images
        ports:
        - name: http
          containerPort: 8001
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 15
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        envFrom:
        - configMapRef:
            name: todo-app-config
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: DATABASE_URL
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: BETTER_AUTH_SECRET
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: OPENAI_API_KEY
              optional: true
        - name: OPENROUTER_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: OPENROUTER_API_KEY
              optional: true
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: GROQ_API_KEY
              optional: true
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: GEMINI_API_KEY
              optional: true
        - name: CLOUDFLARE_R2_ACCOUNT_ID
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: CLOUDFLARE_R2_ACCOUNT_ID
              optional: true
        - name: CLOUDFLARE_R2_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: CLOUDFLARE_R2_ACCESS_KEY_ID
              optional: true
        - name: CLOUDFLARE_R2_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: CLOUDFLARE_R2_SECRET_ACCESS_KEY
              optional: true
        - name: CLOUDFLARE_R2_BUCKET_NAME
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: CLOUDFLARE_R2_BUCKET_NAME
              optional: true
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: false
```

**Validation Rules**:
- `replicas` must be >= 1
- `image` must exist in Minikube Docker daemon
- `imagePullPolicy` must be "Never" for local development
- `containerPort` must be 8001 (avoids conflict with 8000)
- At least one LLM provider API key must be set (OPENAI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, or GEMINI_API_KEY)
- Resource requests must be <= limits
- Security context must enforce non-root execution

**Relationships**:
- References: `todo-app-config` ConfigMap, `todo-app-secrets` Secret
- Managed by: `todo-app-backend` Service
- Exposes: Port 8001 for HTTP traffic
- Connects to: External Neon PostgreSQL database, External Cloudflare R2 storage

**State Transitions**:
1. **Pending** → Waiting for image pull and resource allocation
2. **Running** → Container started, health probes executing
3. **Ready** → Readiness probe passed (database connected), receiving traffic
4. **Failed** → Liveness probe failed or database connection lost, container restarting

---

### 3. Frontend Service

**Entity Name**: `todo-app-frontend` (Service)

**Purpose**: Exposes frontend pods externally via NodePort for browser access

**Fields**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-app-frontend
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: frontend
    app.kubernetes.io/instance: todo-app
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  ports:
  - port: 3000
    targetPort: http
    protocol: TCP
    name: http
    nodePort: 30300
  selector:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: frontend
```

**Validation Rules**:
- `type` must be "NodePort"
- `port` must be 3000 (service port)
- `targetPort` must match container port name "http" (3000)
- `nodePort` must be 30300 (in range 30000-32767)
- Selector labels must match frontend deployment labels

**Relationships**:
- Routes traffic to: `todo-app-frontend` Deployment pods
- Accessed via: `http://<minikube-ip>:30300` or `kubectl port-forward`

**Load Balancing**:
- Distributes traffic across all ready frontend pods
- Removes unhealthy pods from rotation based on readiness probe

---

### 4. Backend Service

**Entity Name**: `todo-app-backend` (Service)

**Purpose**: Exposes backend pods internally via ClusterIP for frontend-to-backend communication

**Fields**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-app-backend
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: backend
    app.kubernetes.io/instance: todo-app
    app.kubernetes.io/managed-by: Helm
spec:
  type: ClusterIP
  ports:
  - port: 8001
    targetPort: http
    protocol: TCP
    name: http
  selector:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: backend
```

**Validation Rules**:
- `type` must be "ClusterIP" (internal only)
- `port` must be 8001 (service port)
- `targetPort` must match container port name "http" (8001)
- Selector labels must match backend deployment labels

**Relationships**:
- Routes traffic to: `todo-app-backend` Deployment pods
- Accessed via: Internal DNS name `todo-app-backend:8001` (from frontend pods)
- Not accessible: From outside the cluster (security requirement)

**Load Balancing**:
- Distributes traffic across all ready backend pods
- Removes unhealthy pods from rotation based on readiness probe

---

### 5. ConfigMap

**Entity Name**: `todo-app-config` (ConfigMap)

**Purpose**: Stores non-sensitive configuration shared across frontend and backend pods

**Fields**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-app-config
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: configuration
    app.kubernetes.io/instance: todo-app
    app.kubernetes.io/managed-by: Helm
data:
  # Service URLs (internal cluster communication)
  FRONTEND_URL: "http://localhost:3000"
  BACKEND_URL: "http://todo-app-backend:8001"

  # LLM Provider configuration
  LLM_PROVIDER: "openai"
  OPENAI_DEFAULT_MODEL: "gpt-4o-mini"
  GEMINI_DEFAULT_MODEL: "gemini-2.5-flash"
  GROQ_DEFAULT_MODEL: "llama-3.3-70b-versatile"
  OPENROUTER_DEFAULT_MODEL: "openai/gpt-4o-mini"

  # Logging
  LOG_LEVEL: "info"
```

**Validation Rules**:
- All values must be strings
- `BACKEND_URL` must use internal service DNS name
- `LLM_PROVIDER` must be one of: "openai", "gemini", "groq", "openrouter"
- `LOG_LEVEL` must be one of: "debug", "info", "warning", "error"

**Relationships**:
- Injected into: Frontend and backend deployments via `envFrom`
- Configurable via: Helm values.yaml and values-dev.yaml

**Update Behavior**:
- Changes require pod restart to take effect
- Helm upgrade automatically triggers rolling update

---

### 6. Secret

**Entity Name**: `todo-app-secrets` (Secret)

**Purpose**: Stores sensitive credentials (base64-encoded) for database, authentication, and LLM providers

**Fields**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/component: secrets
    app.kubernetes.io/instance: todo-app
    app.kubernetes.io/managed-by: Helm
type: Opaque
data:
  # Required secrets (base64-encoded)
  DATABASE_URL: <base64-encoded-value>
  BETTER_AUTH_SECRET: <base64-encoded-value>

  # LLM API keys (at least one required, base64-encoded)
  OPENAI_API_KEY: <base64-encoded-value>
  OPENROUTER_API_KEY: <base64-encoded-value>
  GROQ_API_KEY: <base64-encoded-value>
  GEMINI_API_KEY: <base64-encoded-value>

  # Cloudflare R2 credentials (optional, base64-encoded)
  CLOUDFLARE_R2_ACCOUNT_ID: <base64-encoded-value>
  CLOUDFLARE_R2_ACCESS_KEY_ID: <base64-encoded-value>
  CLOUDFLARE_R2_SECRET_ACCESS_KEY: <base64-encoded-value>
  CLOUDFLARE_R2_BUCKET_NAME: <base64-encoded-value>
```

**Validation Rules**:
- `DATABASE_URL` must be valid PostgreSQL connection string
- `BETTER_AUTH_SECRET` must be minimum 32 characters
- At least one LLM API key must be provided
- All values must be base64-encoded
- Secret must not be committed to version control

**Relationships**:
- Injected into: Frontend and backend deployments via `env` with `secretKeyRef`
- Created by: Helm deployment script using `--set` flags
- Source: `.env` file (loaded by deployment script)

**Security Requirements**:
- Never logged in plaintext
- Never visible in pod environment output
- Passed via Helm `--set` flags during deployment
- Base64 encoding applied automatically by Kubernetes

---

### 7. Helm Chart

**Entity Name**: `todo-app` (Helm Chart)

**Purpose**: Packages all Kubernetes resources with templating and versioning

**Structure**:
```text
helm/todo-app/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Production defaults
├── values-dev.yaml         # Minikube overrides
├── .helmignore             # Exclusion patterns
└── templates/
    ├── _helpers.tpl        # Template helpers
    ├── configmap.yaml      # ConfigMap template
    ├── secret.yaml         # Secret template
    ├── deployment-frontend.yaml
    ├── deployment-backend.yaml
    ├── service-frontend.yaml
    └── service-backend.yaml
```

**Chart.yaml Fields**:
```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for deploying the Todo application with AI chatbot
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - ai
  - chatbot
  - kubernetes
maintainers:
  - name: Todo App Team
```

**Values.yaml (Production Defaults)**:
```yaml
replicaCount:
  frontend: 2
  backend: 2

image:
  frontend:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  backend:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent

service:
  frontend:
    type: NodePort
    port: 3000
    nodePort: 30300
  backend:
    type: ClusterIP
    port: 8001

resources:
  frontend:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
  backend:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

healthProbes:
  frontend:
    liveness:
      initialDelaySeconds: 30
      periodSeconds: 15
      timeoutSeconds: 5
      failureThreshold: 3
    readiness:
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
  backend:
    liveness:
      initialDelaySeconds: 30
      periodSeconds: 15
      timeoutSeconds: 5
      failureThreshold: 3
    readiness:
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3

config:
  BACKEND_URL: "http://todo-app-backend:8001"
  FRONTEND_URL: "http://localhost:3000"
  LLM_PROVIDER: "openai"
  OPENAI_DEFAULT_MODEL: "gpt-4o-mini"
  GEMINI_DEFAULT_MODEL: "gemini-2.5-flash"
  GROQ_DEFAULT_MODEL: "llama-3.3-70b-versatile"
  OPENROUTER_DEFAULT_MODEL: "openai/gpt-4o-mini"
  LOG_LEVEL: "info"

secrets:
  DATABASE_URL: ""
  BETTER_AUTH_SECRET: ""
  OPENAI_API_KEY: ""
  OPENROUTER_API_KEY: ""
  GROQ_API_KEY: ""
  GEMINI_API_KEY: ""
  CLOUDFLARE_R2_ACCOUNT_ID: ""
  CLOUDFLARE_R2_ACCESS_KEY_ID: ""
  CLOUDFLARE_R2_SECRET_ACCESS_KEY: ""
  CLOUDFLARE_R2_BUCKET_NAME: ""
```

**Values-dev.yaml (Minikube Overrides)**:
```yaml
replicaCount:
  frontend: 1
  backend: 1

image:
  frontend:
    pullPolicy: Never  # Use local images only
  backend:
    pullPolicy: Never  # Use local images only

config:
  BACKEND_URL: "http://todo-app-backend:8001"
  FRONTEND_URL: "http://localhost:3000"
  LOG_LEVEL: "debug"
```

**Validation Rules**:
- Chart version must follow semantic versioning
- All templates must be valid YAML
- Template helpers must be defined in _helpers.tpl
- Values must match template expectations

**Relationships**:
- Manages: All Kubernetes resources (Deployments, Services, ConfigMap, Secret)
- Deployed by: `helm upgrade --install` command
- Configured via: values.yaml, values-dev.yaml, and `--set` flags

---

## Resource Relationships Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                         Helm Chart                              │
│  (todo-app v1.0.0)                                              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ ConfigMap    │  │ Secret       │  │ Deployments  │         │
│  │ (config)     │  │ (secrets)    │  │ (frontend +  │         │
│  │              │  │              │  │  backend)    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                 │                  │
│         └─────────────────┴─────────────────┘                  │
│                           │                                     │
│                           ▼                                     │
│         ┌─────────────────────────────────────┐                │
│         │         Pod Templates               │                │
│         │  (envFrom + env injection)          │                │
│         └─────────────────────────────────────┘                │
│                           │                                     │
│         ┌─────────────────┴─────────────────┐                  │
│         ▼                                   ▼                  │
│  ┌──────────────┐                    ┌──────────────┐         │
│  │ Frontend     │                    │ Backend      │         │
│  │ Pods         │                    │ Pods         │         │
│  │ (1-N)        │                    │ (1-N)        │         │
│  └──────┬───────┘                    └──────┬───────┘         │
│         │                                   │                  │
│         ▼                                   ▼                  │
│  ┌──────────────┐                    ┌──────────────┐         │
│  │ Frontend     │                    │ Backend      │         │
│  │ Service      │                    │ Service      │         │
│  │ (NodePort    │                    │ (ClusterIP   │         │
│  │  30300)      │                    │  8001)       │         │
│  └──────┬───────┘                    └──────┬───────┘         │
│         │                                   │                  │
└─────────┼───────────────────────────────────┼──────────────────┘
          │                                   │
          ▼                                   ▼
    External Access                    Internal Access
    (Browser)                          (Frontend → Backend)
    http://<minikube-ip>:30300         http://todo-app-backend:8001
```

---

## External Dependencies

### Neon PostgreSQL Database

**Type**: External managed service (not deployed in cluster)

**Connection**:
- Via `DATABASE_URL` secret
- Format: `postgresql://user:password@host/database?sslmode=require`
- Accessed by: Backend pods only

**Validation**:
- Backend readiness probe tests database connectivity
- Connection failure prevents pod from receiving traffic

### Cloudflare R2 Storage

**Type**: External object storage (not deployed in cluster)

**Connection**:
- Via R2 credentials in secrets (optional)
- Accessed by: Backend pods only (for file uploads)

**Validation**:
- Optional dependency (application works without it)
- Connection errors logged but don't affect readiness

---

## Summary

This data model defines 7 primary Kubernetes resources:
1. **Frontend Deployment** - Next.js pods with health probes
2. **Backend Deployment** - FastAPI pods with health probes
3. **Frontend Service** - NodePort for external access
4. **Backend Service** - ClusterIP for internal communication
5. **ConfigMap** - Non-sensitive configuration
6. **Secret** - Sensitive credentials
7. **Helm Chart** - Packaging and templating

All resources follow Kubernetes best practices:
- Non-root execution (UID 1000)
- Resource limits and requests
- Health probes for automatic recovery
- Secure configuration management
- Standard labels for organization
