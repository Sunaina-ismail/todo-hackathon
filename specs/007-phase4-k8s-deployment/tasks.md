# Tasks: Phase 4 Kubernetes Deployment

**Input**: Design documents from `/specs/007-phase4-k8s-deployment/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/health-endpoints.yaml, quickstart.md

**Organization**: Tasks are grouped by phase to enable systematic deployment infrastructure implementation. Phase 2 (Foundational) BLOCKS all user story phases.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (P1-P7)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `phase-4-k8s-deployment/frontend/`, `phase-4-k8s-deployment/backend/`, `phase-4-k8s-deployment/helm/`, `phase-4-k8s-deployment/scripts/`

---

## Phase 1: Setup (Project Structure)

**Purpose**: Initialize Phase 4 directory structure and configuration files

- [X] T001 Create phase-4-k8s-deployment directory structure with frontend/, backend/, helm/, scripts/, docs/ subdirectories
- [X] T002 [P] Copy Phase 3 frontend code to phase-4-k8s-deployment/frontend/ (preserve all existing functionality)
- [X] T003 [P] Copy Phase 3 backend code to phase-4-k8s-deployment/backend/ (preserve all existing functionality)
- [X] T004 Create .env.example in phase-4-k8s-deployment/ with all required environment variables (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, GEMINI_API_KEY, CLOUDFLARE_R2_*)
- [X] T005 Create .dockerignore files for frontend and backend (exclude node_modules, .next, __pycache__, .env, .git)

**Acceptance Criteria**:
- Directory structure matches plan.md project structure
- All Phase 3 code copied without modifications
- .env.example includes all 11 environment variables from data-model.md
- .dockerignore files prevent unnecessary files in images

---

## Phase 2: Foundational (Health Endpoints + Dockerfiles) ⚠️ BLOCKS ALL USER STORIES

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Frontend Health Endpoints

- [X] T006 [P] [P2] Implement GET /api/health liveness endpoint in phase-4-k8s-deployment/frontend/app/api/health/route.ts (returns 200 OK with {"status": "ok", "timestamp": ISO8601, "service": "frontend"})
- [X] T007 [P] [P2] Implement GET /api/ready readiness endpoint in phase-4-k8s-deployment/frontend/app/api/ready/route.ts (validates DATABASE_URL and BETTER_AUTH_SECRET environment variables, returns 200 with {"status": "ready", "checks": {"environment": "ok", "database": "n/a"}} or 503 with errors array)

### Backend Health Endpoints

- [X] T008 [P] [P2] Implement GET /api/health liveness endpoint in phase-4-k8s-deployment/backend/src/api/health.py (returns 200 OK with {"status": "ok", "timestamp": ISO8601, "service": "backend"})
- [X] T009 [P] [P2] Implement GET /api/ready readiness endpoint in phase-4-k8s-deployment/backend/src/api/health.py (tests database connectivity via SELECT 1, validates environment variables, returns 200 with {"status": "ready", "checks": {"environment": "ok", "database": "ok"}} or 503 with errors array)

### Health Endpoint Tests

- [X] T010 [P] [P2] Create pytest tests for backend health endpoints in phase-4-k8s-deployment/backend/tests/test_health.py (test liveness returns 200, readiness returns 200 with valid DB or 503 without DB)
- [X] T011 [P] [P2] Create Jest tests for frontend health endpoints in phase-4-k8s-deployment/frontend/__tests__/api/health.test.ts (test liveness returns 200, readiness validates env vars)

### Dockerfiles

- [X] T012 [P] [P2] Create multi-stage Dockerfile for frontend in phase-4-k8s-deployment/frontend/Dockerfile (Node 22 Alpine base, non-root user UID 1000, HEALTHCHECK CMD curl -f http://localhost:3000/api/health, optimized layer caching)
- [X] T013 [P] [P2] Create multi-stage Dockerfile for backend in phase-4-k8s-deployment/backend/Dockerfile (Python 3.13 slim base, non-root user UID 1000, HEALTHCHECK CMD curl -f http://localhost:8001/api/health, uv for dependency management)

**Checkpoint**: Foundation ready - health endpoints functional, Dockerfiles build successfully, tests pass

**Acceptance Criteria**:
- All health endpoints return correct status codes and JSON structure per contracts/health-endpoints.yaml
- Backend readiness probe successfully tests database connectivity
- Frontend readiness probe validates required environment variables
- All tests pass (pytest for backend, Jest for frontend)
- Dockerfiles build successfully with `docker build` command
- Images run as non-root user (UID 1000)
- HEALTHCHECK commands work in Docker containers

---

## Phase 3: User Story P1 - Automated Single-Command Deployment 🎯 MVP

**Goal**: Developer can deploy entire application stack with single command in under 10 minutes

**Independent Test**: Run `./scripts/deploy.sh` and verify all pods reach Ready status within 120 seconds

### Helm Chart Structure

- [X] T014 [P] [P1] Create Helm Chart.yaml in phase-4-k8s-deployment/helm/todo-app/Chart.yaml (apiVersion: v2, name: todo-app, version: 1.0.0, appVersion: "1.0.0", description: "Todo application with AI chatbot")
- [X] T015 [P] [P1] Create Helm values.yaml in phase-4-k8s-deployment/helm/todo-app/values.yaml (production defaults: 2 replicas, IfNotPresent pull policy, resource limits per data-model.md)
- [X] T016 [P] [P1] Create Helm values-dev.yaml in phase-4-k8s-deployment/helm/todo-app/values-dev.yaml (Minikube overrides: 1 replica, Never pull policy, debug logging)
- [X] T017 [P] [P1] Create Helm .helmignore in phase-4-k8s-deployment/helm/todo-app/.helmignore (exclude .git, .env, *.md)

### Helm Template Helpers

- [X] T018 [P1] Create Helm template helpers in phase-4-k8s-deployment/helm/todo-app/templates/_helpers.tpl (define todo-app.name, todo-app.fullname, todo-app.labels, todo-app.selectorLabels per data-model.md)

### Helm Templates - Configuration

- [X] T019 [P] [P1] Create ConfigMap template in phase-4-k8s-deployment/helm/todo-app/templates/configmap.yaml (BACKEND_URL: http://todo-app-backend:8001, FRONTEND_URL: http://localhost:3000, LLM_PROVIDER, model names, LOG_LEVEL per data-model.md)
- [X] T020 [P] [P1] Create Secret template in phase-4-k8s-deployment/helm/todo-app/templates/secret.yaml (DATABASE_URL, BETTER_AUTH_SECRET, LLM API keys, R2 credentials - all from values with base64 encoding)

### Helm Templates - Deployments

- [X] T021 [P] [P1] Create frontend deployment template in phase-4-k8s-deployment/helm/todo-app/templates/deployment-frontend.yaml (replicas from values, image: todo-frontend:latest with Never pull policy, security context UID 1000, liveness probe /api/health initialDelaySeconds=30 periodSeconds=15, readiness probe /api/ready initialDelaySeconds=10 periodSeconds=10, resource limits 500m CPU 512Mi memory, envFrom configMapRef, env from secretKeyRef for DATABASE_URL and BETTER_AUTH_SECRET)
- [X] T022 [P] [P1] Create backend deployment template in phase-4-k8s-deployment/helm/todo-app/templates/deployment-backend.yaml (replicas from values, image: todo-backend:latest with Never pull policy, security context UID 1000, liveness probe /api/health initialDelaySeconds=30 periodSeconds=15, readiness probe /api/ready initialDelaySeconds=10 periodSeconds=10, resource limits 500m CPU 512Mi memory, envFrom configMapRef, env from secretKeyRef for all secrets with optional: true for LLM keys)

### Helm Templates - Services

- [X] T023 [P] [P1] Create frontend service template in phase-4-k8s-deployment/helm/todo-app/templates/service-frontend.yaml (type: NodePort, port: 3000, targetPort: http, nodePort: 30300, selector matches frontend deployment labels)
- [X] T024 [P] [P1] Create backend service template in phase-4-k8s-deployment/helm/todo-app/templates/service-backend.yaml (type: ClusterIP, port: 8001, targetPort: http, selector matches backend deployment labels)

### Deployment Script

- [X] T025 [P1] Create deployment script in phase-4-k8s-deployment/scripts/deploy.sh (bash script with set -e, 10 steps: validate prerequisites with command -v checks for minikube/helm/docker/kubectl, check minikube status with `minikube status`, start minikube if not running with `minikube start`, configure Docker daemon with `eval $(minikube docker-env)`, build frontend image with `docker build -t todo-frontend:latest ./frontend`, build backend image with `docker build -t todo-backend:latest ./backend`, load .env file and validate required variables, create namespace with `kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -`, deploy with `helm upgrade --install todo-app ./helm/todo-app -f ./helm/todo-app/values-dev.yaml -n todo-app --set secrets.DATABASE_URL=$DATABASE_URL --set secrets.BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET --set secrets.OPENAI_API_KEY=$OPENAI_API_KEY`, wait for pods with `kubectl wait --for=condition=ready pod --all -n todo-app --timeout=120s`, display access instructions with minikube ip and port-forward commands)
- [X] T026 [P1] Make deploy.sh executable with `chmod +x phase-4-k8s-deployment/scripts/deploy.sh`

**Checkpoint**: Deployment script completes successfully, all pods reach Ready status within 120 seconds

**Acceptance Criteria**:
- Helm chart validates with `helm lint ./helm/todo-app`
- Helm templates render correctly with `helm template todo-app ./helm/todo-app -f ./helm/todo-app/values-dev.yaml`
- Deployment script completes in under 10 minutes (FR-013)
- All prerequisite checks pass before proceeding
- Docker images build successfully in Minikube daemon
- Helm deployment succeeds without errors
- All pods reach Ready status within 120 seconds (FR-055, SC-002)
- Access instructions display correct URLs for port-forward and NodePort

---

## Phase 4: User Story P2 - Health Monitoring and Auto-Recovery

**Goal**: Failed pods automatically restart within 30 seconds, unhealthy pods removed from service

**Independent Test**: Kill a pod with `kubectl delete pod -n todo-app <pod-name>` and verify automatic restart within 30 seconds

**Note**: Health endpoints and probes already implemented in Phase 2 (Foundational). This phase adds verification and documentation.

### Health Monitoring Verification

- [X] T027 [P2] Create health monitoring verification script in phase-4-k8s-deployment/scripts/verify-health.sh (test liveness probe triggers restart by exec into pod and killing process, test readiness probe removes pod from service by breaking database connection, verify pod restarts within 30 seconds, verify unhealthy pods removed from service endpoints)

**Checkpoint**: Health probes working correctly, automatic recovery verified

**Acceptance Criteria**:
- Liveness probe detects failed pods and triggers restart within 30 seconds (FR-023, SC-005)
- Readiness probe prevents traffic to pods that are not ready (FR-024)
- Verification script confirms both probe types work correctly
- Pod events show probe failures and restart actions

---

## Phase 5: User Story P3 - Secure Configuration Management

**Goal**: Zero secrets or API keys visible in deployment logs or pod environment output

**Independent Test**: Run `kubectl logs -n todo-app <pod-name>` and `kubectl exec -n todo-app <pod-name> -- env` and verify no secrets in plaintext

**Note**: ConfigMaps and Secrets already implemented in Phase 3 (P1). This phase adds security verification.

### Security Verification

- [X] T028 [P3] Create security verification script in phase-4-k8s-deployment/scripts/verify-security.sh (check deployment logs with `kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app --tail=100` for secrets, check pod environment with `kubectl exec -n todo-app deployment/todo-app-backend -- env` for plaintext secrets, verify all secrets are base64-encoded in Secret resource with `kubectl get secret todo-app-secrets -n todo-app -o yaml`, confirm no secrets in Git history with `git log --all --full-history --source -- **/.env`)

**Checkpoint**: Security verification passes, no secrets exposed

**Acceptance Criteria**:
- Deployment logs do not expose secrets or API keys in plaintext (FR-030, SC-006)
- Pod environment output does not expose secrets in plaintext (FR-031)
- All secrets stored in Kubernetes Secret resource with base64 encoding
- .env file not committed to Git (in .gitignore)
- Verification script confirms all security requirements

---

## Phase 6: User Story P4 - Network Access and Service Exposure

**Goal**: Frontend accessible via NodePort and port-forward, backend internal only

**Independent Test**: Access frontend at `http://<minikube-ip>:30300` and via `kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app`, verify backend not accessible externally

**Note**: Services already implemented in Phase 3 (P1). This phase adds network verification and access documentation.

### Network Verification

- [X] T029 [P4] Create network verification script in phase-4-k8s-deployment/scripts/verify-network.sh (get minikube IP with `minikube ip`, test frontend NodePort access with `curl http://$(minikube ip):30300/api/health`, test port-forward with `kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app --address 0.0.0.0` in background and curl localhost:3000, verify backend ClusterIP not externally accessible, test internal backend access from frontend pod with `kubectl exec -n todo-app deployment/todo-app-frontend -- curl http://todo-app-backend:8001/api/health`)

**Checkpoint**: Network access working correctly, frontend accessible externally, backend internal only

**Acceptance Criteria**:
- Frontend accessible via NodePort on port 30300 (FR-014, SC-011)
- Frontend accessible via kubectl port-forward (FR-016)
- Backend accessible from frontend pods via internal DNS (FR-018)
- Backend NOT accessible from outside cluster (security requirement)
- Verification script confirms all network requirements

---

## Phase 7: User Story P5 - Horizontal Pod Scaling

**Goal**: Frontend and backend scale independently without service disruption

**Independent Test**: Scale frontend to 3 replicas with `kubectl scale deployment -n todo-app todo-app-frontend --replicas=3`, verify all replicas reach Ready status and receive traffic

### Scaling Verification

- [X] T030 [P5] Create scaling verification script in phase-4-k8s-deployment/scripts/verify-scaling.sh (scale frontend to 3 replicas with `kubectl scale deployment -n todo-app todo-app-frontend --replicas=3`, wait for rollout with `kubectl rollout status deployment -n todo-app todo-app-frontend`, verify all 3 pods ready with `kubectl get pods -n todo-app -l app.kubernetes.io/component=frontend`, test load balancing by curling service multiple times and checking pod logs, scale backend to 2 replicas with `kubectl scale deployment -n todo-app todo-app-backend --replicas=2`, verify no service disruption during scaling, scale back to 1 replica each)

**Checkpoint**: Scaling works correctly, no service disruption

**Acceptance Criteria**:
- Frontend scales from 1 to 3 replicas without service disruption (FR-049, SC-007)
- Backend scales from 1 to 2 replicas without service disruption (FR-050)
- All new replicas reach Ready status within 120 seconds (SC-004)
- Service load balances traffic across all replicas
- Scaling down does not cause errors
- Verification script confirms all scaling requirements

---

## Phase 8: User Story P6 - AI-Assisted DevOps Documentation

**Goal**: Documentation includes at least 3 working kubectl-ai examples, 3 kagent examples, 2 Docker AI examples

**Independent Test**: Run each documented example and verify it executes successfully

### AI DevOps Documentation

- [X] T031 [P] [P6] Create kubectl-ai examples in phase-4-k8s-deployment/docs/kubectl-ai-examples.md (example 1: "show me all pods in todo-app namespace that are not ready", example 2: "describe the frontend deployment and explain the health probes", example 3: "show me the logs from the backend pod for the last 5 minutes", include expected output and explanation for each)
- [X] T032 [P] [P6] Create kagent examples in phase-4-k8s-deployment/docs/kagent-guide.md (example 1: automated pod restart diagnostics with kagent analyzing pod events and logs, example 2: resource usage monitoring with kagent checking CPU/memory across all pods, example 3: health probe failure analysis with kagent investigating readiness probe failures, include setup instructions and expected output)
- [X] T033 [P] [P6] Create Docker AI examples in phase-4-k8s-deployment/docs/docker-ai-optimization.md (example 1: image size optimization with Docker AI analyzing Dockerfile and suggesting layer improvements, example 2: security scanning with Docker AI checking for vulnerabilities in base images, include commands and expected recommendations)

**Checkpoint**: AI DevOps documentation complete with working examples

**Acceptance Criteria**:
- kubectl-ai examples document includes at least 3 working examples (FR-062, SC-008)
- kagent guide includes at least 3 working examples (FR-063, SC-009)
- Docker AI optimization includes at least 2 working examples (FR-064, SC-010)
- All examples tested and verified to work
- Documentation includes setup instructions and expected output

---

## Phase 9: User Story P7 - Phase 3 Feature Parity

**Goal**: All Phase 3 features work without regression (authentication, task management, AI chatbot)

**Independent Test**: Complete full user workflow: signup → signin → create task → chat with AI → mark task complete → delete task

### Feature Parity Verification

- [X] T034 [P7] Create feature parity test script in phase-4-k8s-deployment/scripts/verify-phase3-features.sh (test authentication: signup with curl POST to /api/auth/signup, signin with curl POST to /api/auth/signin, verify JWT token in response; test task management: create task with POST /api/tasks, list tasks with GET /api/tasks, update task with PATCH /api/tasks/:id, delete task with DELETE /api/tasks/:id; test AI chatbot: send message to chatbot endpoint, verify response includes task operations, check conversation persistence in database)
- [X] T035 [P7] Update README.md in phase-4-k8s-deployment/README.md (Phase 4 overview, prerequisites, quick start with deploy.sh, access instructions for WSL2/Windows/Linux/Mac, troubleshooting guide, scaling instructions, cleanup instructions, link to quickstart.md)

**Checkpoint**: All Phase 3 features working correctly in Kubernetes deployment

**Acceptance Criteria**:
- All Phase 3 authentication features work without regression (FR-058)
- All Phase 3 task management features work without regression (FR-059)
- All Phase 3 AI chatbot features work without regression (FR-060)
- All Phase 3 user workflows complete successfully (FR-061, SC-004)
- Feature parity test script passes all checks
- README.md provides clear deployment and access instructions

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [X] T036 [P] Update CLAUDE.md with Phase 4 technologies (Minikube, Helm, Kubernetes, kubectl, Docker, health probes, ConfigMaps, Secrets)
- [X] T037 [P] Create troubleshooting guide in phase-4-k8s-deployment/docs/troubleshooting.md (common issues: pods not starting, health probes failing, cannot access frontend, backend not accessible from frontend, image pull errors, secret exposure, port conflicts, WSL2 networking issues, Helm chart validation errors - with solutions per plan.md risk analysis)
- [X] T038 Run complete quickstart.md verification (all 6 verification steps from quickstart.md: verify pods running, verify services exposed, verify health probes, verify readiness probes, access frontend application, test Phase 3 features)
- [X] T039 Create uninstall script in phase-4-k8s-deployment/scripts/uninstall.sh (helm uninstall todo-app -n todo-app, kubectl delete namespace todo-app, verify cleanup with kubectl get all -n todo-app)
- [X] T040 [P] Add deployment metrics logging to deploy.sh (track deployment start time, image build time, helm deployment time, pod ready time, total deployment time, display metrics summary at end)

**Acceptance Criteria**:
- CLAUDE.md updated with Phase 4 context
- Troubleshooting guide covers all risks from plan.md
- Quickstart.md verification passes all steps
- Uninstall script cleanly removes all resources
- Deployment metrics show completion under 10 minutes (SC-001)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story P1 (Phase 3)**: Depends on Foundational (Phase 2) - Automated deployment
- **User Story P2 (Phase 4)**: Depends on Foundational (Phase 2) - Health monitoring verification
- **User Story P3 (Phase 5)**: Depends on P1 (Phase 3) - Security verification
- **User Story P4 (Phase 6)**: Depends on P1 (Phase 3) - Network verification
- **User Story P5 (Phase 7)**: Depends on P1 (Phase 3) - Scaling verification
- **User Story P6 (Phase 8)**: Depends on P1 (Phase 3) - AI DevOps documentation
- **User Story P7 (Phase 9)**: Depends on P1 (Phase 3) - Feature parity verification
- **Polish (Phase 10)**: Depends on all user stories being complete

### Critical Path

1. **Phase 1 (Setup)** → 2. **Phase 2 (Foundational)** → 3. **Phase 3 (P1 Deployment)** → 4. **Phases 4-9 (P2-P7 in parallel)** → 5. **Phase 10 (Polish)**

### Parallel Opportunities

- **Phase 1**: T002 and T003 can run in parallel (copying frontend and backend code)
- **Phase 2**: T006-T007 (frontend health), T008-T009 (backend health), T010-T011 (tests), T012-T013 (Dockerfiles) can all run in parallel
- **Phase 3**: T014-T017 (Helm structure), T019-T020 (ConfigMap/Secret), T021-T022 (deployments), T023-T024 (services) can run in parallel within their groups
- **Phases 4-9**: Once P1 (Phase 3) completes, P2-P7 (Phases 4-9) can all run in parallel
- **Phase 10**: T036-T037 can run in parallel

---

## Implementation Strategy

### MVP First (P1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story P1 (Automated Deployment)
4. **STOP and VALIDATE**: Run deploy.sh and verify all pods reach Ready status
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add P1 (Automated Deployment) → Test independently → Deploy/Demo (MVP!)
3. Add P2 (Health Monitoring) → Test independently → Deploy/Demo
4. Add P3 (Security) → Test independently → Deploy/Demo
5. Add P4 (Network) → Test independently → Deploy/Demo
6. Add P5 (Scaling) → Test independently → Deploy/Demo
7. Add P6 (AI DevOps Docs) → Test independently → Deploy/Demo
8. Add P7 (Feature Parity) → Test independently → Deploy/Demo
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Team completes P1 (Automated Deployment) together
3. Once P1 is done:
   - Developer A: P2 (Health Monitoring)
   - Developer B: P3 (Security)
   - Developer C: P4 (Network)
   - Developer D: P5 (Scaling)
   - Developer E: P6 (AI DevOps Docs)
   - Developer F: P7 (Feature Parity)
4. Stories complete and integrate independently

---

## Command Validation (Context7 MCP)

All kubectl, Helm, and Minikube commands used in tasks have been validated against official documentation:

**Helm Commands** (validated via /websites/helm_sh):
- `helm upgrade --install <release> -f <values> <chart>` - Install or upgrade release
- `helm lint <chart>` - Validate chart syntax
- `helm template <chart> -f <values>` - Render templates locally
- `helm uninstall <release> -n <namespace>` - Remove release

**Kubectl Commands** (validated via /websites/kubernetes_io):
- `kubectl get pods -n <namespace>` - List pods
- `kubectl describe pod <pod> -n <namespace>` - Show pod details
- `kubectl logs -n <namespace> <pod>` - View pod logs
- `kubectl port-forward svc/<service> <port>:<port> -n <namespace>` - Forward service port
- `kubectl scale deployment <deployment> --replicas=<n> -n <namespace>` - Scale deployment
- `kubectl exec -n <namespace> <pod> -- <command>` - Execute command in pod
- `kubectl wait --for=condition=ready pod --all -n <namespace> --timeout=<time>` - Wait for pods

**Minikube Commands** (validated via /websites/minikube_sigs_k8s_io):
- `minikube start` - Start local cluster
- `minikube status` - Check cluster status
- `eval $(minikube docker-env)` - Configure Docker to use Minikube daemon
- `minikube ip` - Get cluster IP address
- `minikube service <service> -n <namespace>` - Access service via browser

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (P1-P7)
- Phase 2 (Foundational) MUST be complete before any user story work begins
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All commands validated via Context7 MCP against official documentation
- Backend uses port 8001 (8000 already in use per plan.md)
- Frontend NodePort uses 30300 (in valid range 30000-32767)
- All containers run as non-root user UID 1000
- Resource limits: 500m CPU, 512Mi memory per pod
- Health probe timing: liveness 30s initial/15s period, readiness 10s initial/10s period
