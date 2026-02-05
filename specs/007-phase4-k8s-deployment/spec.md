# Feature Specification: Phase 4 Kubernetes Deployment

**Feature Branch**: `007-phase4-k8s-deployment`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Deploy Phase 3 AI-powered Todo application (FastAPI backend with OpenAI Agents SDK + Next.js ChatKit frontend) to local Minikube Kubernetes cluster with production-ready infrastructure."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Single-Command Deployment (Priority: P1)

As a developer, I want to deploy the entire Todo application stack (FastAPI backend with OpenAI Agents SDK, Next.js frontend with ChatKit) to a local Minikube Kubernetes cluster using a single automated command, so that I can quickly provision a production-like environment for testing without manual configuration steps.

**Why this priority**: This is the foundation that enables all other stories. Without automated deployment, developers cannot efficiently test or validate any other Kubernetes features. This directly impacts development velocity and reduces deployment errors.

**Independent Test**: Run the deployment script and verify that both frontend and backend pods reach Ready status within 120 seconds. Access the application via port-forward and confirm Phase 3 features work (login, create task, chat with AI).

**Acceptance Scenarios**:

1. **Given** a clean Minikube environment with no existing deployments, **When** developer runs the deployment script with valid environment variables, **Then** the script completes successfully in under 10 minutes and all pods reach Ready status
2. **Given** Minikube is not running, **When** developer runs the deployment script, **Then** the script automatically starts Minikube and proceeds with deployment
3. **Given** required environment variables are missing, **When** developer runs the deployment script, **Then** the script fails with clear error messages indicating which variables are missing
4. **Given** a successful deployment, **When** developer runs `kubectl get pods -n todo-app`, **Then** all pods show status "Running" with "1/1" ready containers

---

### User Story 2 - Health Monitoring and Auto-Recovery (Priority: P2)

As a developer, I want all application pods to have comprehensive health monitoring (liveness and readiness probes), so that Kubernetes can automatically detect and restart failed containers without manual intervention, ensuring high availability.

**Why this priority**: Health monitoring is critical for production readiness. Without it, failed pods would remain in a broken state, requiring manual intervention. This is essential for validating that the application can self-heal in production.

**Independent Test**: Manually kill a backend pod process and verify that Kubernetes detects the failure via liveness probe and restarts the pod within 30 seconds. Verify that readiness probe prevents traffic to pods that aren't ready (e.g., when database connection fails).

**Acceptance Scenarios**:

1. **Given** a running backend pod, **When** the pod's main process crashes, **Then** the liveness probe detects the failure and Kubernetes restarts the pod within 30 seconds
2. **Given** a backend pod starting up, **When** the database connection is not yet established, **Then** the readiness probe fails and the pod does not receive traffic until the connection succeeds
3. **Given** a frontend pod with invalid environment variables, **When** the readiness probe checks the pod, **Then** the probe fails and the pod is marked as not ready
4. **Given** all pods are healthy, **When** checking pod status, **Then** both liveness and readiness probes show success status

---

### User Story 3 - Secure Configuration Management (Priority: P3)

As a developer, I want environment variables and secrets managed through Kubernetes ConfigMaps and Secrets, so that sensitive credentials are never hardcoded, configuration is centralized, and deployment logs never expose secrets in plaintext.

**Why this priority**: Security is non-negotiable. Hardcoded secrets or exposed credentials in logs create serious security vulnerabilities. This must be implemented before any production deployment.

**Independent Test**: Deploy the application and verify that DATABASE_URL, BETTER_AUTH_SECRET, and API keys are stored in Kubernetes Secrets. Check pod logs and environment output to confirm no secrets are visible in plaintext.

**Acceptance Scenarios**:

1. **Given** secrets are defined in .env file, **When** deployment script runs, **Then** secrets are created in Kubernetes Secret resource and injected into pods as environment variables
2. **Given** non-sensitive configuration (log level, service URLs), **When** deployment runs, **Then** configuration is stored in ConfigMap and injected into pods
3. **Given** a running pod, **When** checking pod logs with `kubectl logs`, **Then** no secrets or API keys are visible in plaintext
4. **Given** a running pod, **When** executing `kubectl exec pod -- env`, **Then** secrets are present as environment variables but not visible in deployment manifests

---

### User Story 4 - Network Access and Service Exposure (Priority: P4)

As a developer, I want to access the frontend application through kubectl port-forward and NodePort service on port 30300, while the backend communicates internally via ClusterIP on port 8001, so that I can test the application from my local machine while maintaining secure internal communication.

**Why this priority**: Without proper network access, developers cannot test the deployed application. Port-forwarding provides a secure, flexible way to access services without exposing them externally.

**Independent Test**: After deployment, run `kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app` and access the application at http://localhost:3000. Verify that the frontend can communicate with the backend via internal ClusterIP service.

**Acceptance Scenarios**:

1. **Given** a successful deployment, **When** developer runs kubectl port-forward to frontend service, **Then** the application is accessible at localhost:3000 and all features work
2. **Given** frontend and backend pods are running, **When** frontend makes API calls to backend, **Then** requests route through internal ClusterIP service on port 8001
3. **Given** NodePort service is configured, **When** accessing frontend via Minikube IP and port 30300, **Then** the application loads successfully
4. **Given** backend service is ClusterIP, **When** attempting to access backend from outside the cluster, **Then** the backend is not accessible (internal only)

---

### User Story 5 - Horizontal Pod Scaling (Priority: P5)

As a developer, I want the system to support horizontal pod scaling, so that I can independently scale frontend and backend replicas to test load distribution and validate that the application works correctly with multiple instances.

**Why this priority**: Scalability testing is important for production readiness. Being able to scale pods independently validates that the application is truly stateless and can handle distributed deployments.

**Independent Test**: Scale frontend to 3 replicas and backend to 2 replicas using `kubectl scale` or Helm values. Verify that all replicas reach Ready status and traffic is distributed across pods.

**Acceptance Scenarios**:

1. **Given** a deployment with 1 frontend replica, **When** scaling to 3 replicas via `kubectl scale deployment todo-app-frontend --replicas=3`, **Then** all 3 pods reach Ready status within 120 seconds
2. **Given** multiple backend replicas, **When** frontend makes API calls, **Then** requests are load-balanced across backend pods
3. **Given** scaled deployments, **When** a pod is deleted, **Then** Kubernetes automatically creates a replacement pod
4. **Given** Helm values configured for replica counts, **When** upgrading the Helm release with new replica values, **Then** deployments scale to the specified counts

---

### User Story 6 - AI-Assisted DevOps Documentation (Priority: P6)

As a developer, I want comprehensive documentation for AI-assisted DevOps workflows using kubectl-ai, kagent, and Docker AI (Gordon), so that I can leverage AI tools for troubleshooting, cluster management, and image optimization.

**Why this priority**: AI-assisted tools significantly improve developer productivity and troubleshooting efficiency. Documentation ensures developers can leverage these tools effectively.

**Independent Test**: Follow documentation examples to use kubectl-ai for pod troubleshooting, kagent for cluster health analysis, and Docker AI for image optimization. Verify that all examples work as documented.

**Acceptance Scenarios**:

1. **Given** kubectl-ai is installed, **When** following documentation examples, **Then** kubectl-ai successfully diagnoses pod issues and provides actionable recommendations
2. **Given** kagent is installed, **When** running cluster health analysis, **Then** kagent provides insights into resource usage and potential issues
3. **Given** Docker AI (Gordon) is available, **When** following image optimization examples, **Then** Docker AI provides recommendations for reducing image size and improving security
4. **Given** documentation includes at least 3 examples per tool, **When** developers follow the examples, **Then** all examples execute successfully

---

### User Story 7 - Phase 3 Feature Parity (Priority: P7)

As a developer, I want all Phase 3 features (authentication, task management, AI chatbot) to continue working without any regression or functional degradation, so that the Kubernetes deployment is a transparent infrastructure change that doesn't impact user experience.

**Why this priority**: Regression prevention is critical. Users should not experience any functional differences between Phase 3 and Phase 4 deployments. This validates that the Kubernetes migration is purely an infrastructure improvement.

**Independent Test**: After Kubernetes deployment, execute the complete Phase 3 test suite: user signup/signin, create/read/update/delete tasks, AI chatbot conversations, natural language task management. All tests must pass with identical behavior to Phase 3.

**Acceptance Scenarios**:

1. **Given** a Kubernetes-deployed application, **When** a user signs up with email and password, **Then** the account is created successfully and the user can sign in
2. **Given** an authenticated user, **When** performing CRUD operations on tasks, **Then** all operations work identically to Phase 3 (create, read, update, delete, mark complete)
3. **Given** an authenticated user, **When** opening the AI chatbot and sending natural language commands, **Then** the chatbot responds correctly and executes task operations
4. **Given** Phase 3 test suite, **When** running all tests against Kubernetes deployment, **Then** 100% of tests pass with no regressions

---

### Edge Cases

- **What happens when database connection fails during pod startup?** The backend readiness probe should fail, preventing the pod from receiving traffic. The pod remains in "Not Ready" state until database connectivity is restored. Kubernetes does not route requests to unhealthy pods.

- **What happens when a pod crashes during an active user session?** The liveness probe detects the failure and Kubernetes restarts the pod within 30 seconds. The user's session may be interrupted and they may need to refresh their browser. Stateless architecture ensures no data loss.

- **What happens when secrets are missing or invalid?** Pods fail to start with clear error messages in pod logs indicating which secrets are missing. The deployment script should validate required secrets before attempting deployment.

- **What happens when Minikube runs out of resources?** Pods remain in "Pending" state with resource limit errors visible in pod events. The deployment script should check Minikube resource allocation and warn if insufficient resources are available.

- **What happens when health probe endpoints return errors?** Pods are marked as "Not Ready" and removed from service load balancing. For liveness probes, repeated failures trigger pod restarts. For readiness probes, pods remain running but don't receive traffic.

- **What happens when trying to scale to more replicas than Minikube can handle?** Additional pods remain in "Pending" state with resource warnings. Kubernetes scheduler cannot place pods due to insufficient CPU/memory. Developers should monitor resource usage and adjust Minikube allocation.

- **What happens when Docker images fail to build within Minikube?** The deployment script should detect build failures and exit with clear error messages. Common causes include missing dependencies, syntax errors in Dockerfiles, or insufficient disk space.

- **What happens when Helm chart values are misconfigured?** Helm validation should catch syntax errors before deployment. Runtime errors (e.g., invalid port numbers, missing required values) cause pod failures with descriptive error messages in pod events.

- **What happens when port 8001 is already in use on the host?** Port forwarding will fail with "address already in use" error. Developers should either stop the conflicting service or use a different local port for port-forwarding (e.g., `kubectl port-forward svc/backend 8002:8001`).

- **What happens when external dependencies (Neon database, Cloudflare R2) are unavailable?** Backend pods fail readiness probes and don't receive traffic. Application remains unavailable until external dependencies are restored. Error messages in logs should clearly indicate connection failures to external services.

## Requirements *(mandatory)*

### Functional Requirements

**Deployment Infrastructure:**

- **FR-001**: System MUST deploy on Minikube version 1.32 or higher with Kubernetes 1.28 or higher
- **FR-002**: System MUST use Helm 3.x for deployment packaging and versioning
- **FR-003**: System MUST provide a single automated deployment script that provisions the entire stack
- **FR-004**: Deployment script MUST validate prerequisites (minikube, helm, docker, kubectl) before proceeding
- **FR-005**: Deployment script MUST automatically start Minikube if not running
- **FR-006**: Deployment script MUST configure Docker to use Minikube's internal daemon via `eval $(minikube docker-env)`
- **FR-007**: Deployment script MUST build Docker images within Minikube (no external registry required)
- **FR-008**: Deployment script MUST load environment variables from .env file
- **FR-009**: Deployment script MUST create Kubernetes namespace for the application
- **FR-010**: Deployment script MUST deploy application using Helm with appropriate values
- **FR-011**: Deployment script MUST wait for pods to reach Ready status before completing
- **FR-012**: Deployment script MUST display access instructions including port-forward command
- **FR-013**: Deployment script MUST complete full stack provisioning in under 10 minutes

**Network Services:**

- **FR-014**: Frontend deployment MUST expose NodePort service on port 30300 for external access
- **FR-015**: Backend deployment MUST use ClusterIP service on port 8001 for internal communication only
- **FR-016**: System MUST support kubectl port-forward for accessing frontend service
- **FR-017**: Frontend service MUST route traffic to healthy frontend pods only
- **FR-018**: Backend service MUST route traffic to healthy backend pods only

**Health Monitoring:**

- **FR-019**: Frontend pods MUST implement liveness probe at /api/health endpoint
- **FR-020**: Frontend pods MUST implement readiness probe at /api/ready endpoint that validates environment variables
- **FR-021**: Backend pods MUST implement liveness probe at /api/health endpoint
- **FR-022**: Backend pods MUST implement readiness probe at /api/ready endpoint that tests database connectivity
- **FR-023**: Liveness probes MUST detect failed pods and trigger automatic restarts within 30 seconds
- **FR-024**: Readiness probes MUST prevent traffic to pods that are not ready to serve requests
- **FR-025**: Health probe timing MUST be configurable via Helm values

**Configuration Management:**

- **FR-026**: All sensitive credentials (DATABASE_URL, BETTER_AUTH_SECRET, API keys) MUST be stored in Kubernetes Secrets
- **FR-027**: All non-sensitive configuration (log level, service URLs, LLM provider) MUST be stored in Kubernetes ConfigMaps
- **FR-028**: Secrets MUST be injected into pods as environment variables at runtime
- **FR-029**: ConfigMaps MUST be injected into pods as environment variables at runtime
- **FR-030**: Deployment logs MUST NOT expose secrets or API keys in plaintext
- **FR-031**: Pod environment output MUST NOT expose secrets in plaintext when viewed via kubectl

**Container Images:**

- **FR-032**: Frontend Dockerfile MUST use multi-stage build with Node 22 Alpine base image
- **FR-033**: Backend Dockerfile MUST use multi-stage build with Python 3.13 slim base image
- **FR-034**: All containers MUST run as non-root user (UID 1000)
- **FR-035**: All containers MUST have resource limits (CPU and memory) defined
- **FR-036**: Container images MUST be optimized for size and security

**Helm Charts:**

- **FR-037**: Helm chart MUST include deployment manifests for frontend and backend
- **FR-038**: Helm chart MUST include service manifests for frontend (NodePort) and backend (ClusterIP)
- **FR-039**: Helm chart MUST include ConfigMap manifest for non-sensitive configuration
- **FR-040**: Helm chart MUST include Secret manifest for sensitive credentials
- **FR-041**: Helm chart MUST have values.yaml with production defaults
- **FR-042**: Helm chart MUST have values-dev.yaml with Minikube-specific overrides
- **FR-043**: Helm chart MUST support replica count configuration via values
- **FR-044**: Helm chart MUST support resource limits configuration via values
- **FR-045**: Helm chart MUST support health probe timing configuration via values

**Scalability:**

- **FR-046**: All pods MUST be stateless with no persistent volume claims
- **FR-047**: System MUST support horizontal pod scaling for frontend independently
- **FR-048**: System MUST support horizontal pod scaling for backend independently
- **FR-049**: Frontend pods MUST scale from 1 to N replicas without service disruption
- **FR-050**: Backend pods MUST scale from 1 to N replicas without service disruption

**External Dependencies:**

- **FR-051**: Database (Neon PostgreSQL) MUST remain as external dependency outside the cluster
- **FR-052**: Object storage (Cloudflare R2) MUST remain as external dependency outside the cluster
- **FR-053**: Backend pods MUST connect to external Neon database via DATABASE_URL secret
- **FR-054**: Backend pods MUST connect to external Cloudflare R2 via R2 credentials in secrets

**Performance:**

- **FR-055**: Frontend and backend containers MUST achieve Ready status within 120 seconds of deployment start
- **FR-056**: Frontend MUST respond to HTTP requests within 5 seconds after pod readiness
- **FR-057**: Backend MUST respond to internal API requests within 5 seconds after pod readiness

**Phase 3 Feature Parity:**

- **FR-058**: All Phase 3 authentication features MUST work without regression (signup, signin, JWT validation)
- **FR-059**: All Phase 3 task management features MUST work without regression (CRUD operations, filtering, sorting)
- **FR-060**: All Phase 3 AI chatbot features MUST work without regression (natural language commands, conversation persistence, MCP tools)
- **FR-061**: All Phase 3 user workflows MUST complete successfully with identical behavior

**Documentation:**

- **FR-062**: Documentation MUST include at least 3 working kubectl-ai examples for cluster operations
- **FR-063**: Documentation MUST include at least 3 working kagent examples for automated diagnostics
- **FR-064**: Documentation MUST include at least 2 working Docker AI (Gordon) examples for image optimization
- **FR-065**: Documentation MUST include troubleshooting guide for common deployment issues
- **FR-066**: Documentation MUST include instructions for accessing the application via port-forward
- **FR-067**: Documentation MUST include instructions for scaling pods independently

### Key Entities

- **Frontend Deployment**: Kubernetes Deployment resource for Next.js 16 application with ChatKit UI, configured with health probes, resource limits, and ConfigMap/Secret injection
- **Backend Deployment**: Kubernetes Deployment resource for FastAPI application with OpenAI Agents SDK and MCP tools, configured with health probes, resource limits, and ConfigMap/Secret injection
- **Frontend Service**: Kubernetes NodePort Service exposing port 30300 for external access to frontend pods
- **Backend Service**: Kubernetes ClusterIP Service on port 8001 for internal communication between frontend and backend pods
- **ConfigMap**: Kubernetes ConfigMap storing non-sensitive configuration (LLM provider, log level, service URLs, CORS origins)
- **Secret**: Kubernetes Secret storing sensitive credentials (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, GEMINI_API_KEY, Cloudflare R2 credentials)
- **Helm Chart**: Helm 3.x chart packaging all Kubernetes resources with values.yaml (production defaults) and values-dev.yaml (Minikube overrides)
- **Deployment Script**: Automated bash script that validates prerequisites, starts Minikube, builds images, deploys with Helm, and displays access instructions

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developer can deploy entire application stack with single command in under 10 minutes
- **SC-002**: All pods reach Ready state within 120 seconds of deployment start
- **SC-003**: Frontend responds to HTTP requests within 5 seconds after pod readiness
- **SC-004**: All Phase 3 features work without regression (100% feature parity validated by test suite)
- **SC-005**: Failed pods automatically restart within 30 seconds via liveness probe detection
- **SC-006**: Zero secrets or API keys visible in deployment logs or pod environment output
- **SC-007**: Developer can scale frontend and backend pods independently without service disruption
- **SC-008**: Documentation includes at least 3 working kubectl-ai examples that execute successfully
- **SC-009**: Documentation includes at least 3 working kagent examples that execute successfully
- **SC-010**: Documentation includes at least 2 working Docker AI examples that execute successfully
- **SC-011**: Port forwarding works successfully for accessing frontend at localhost:3000
- **SC-012**: Backend communicates with frontend via internal ClusterIP service without external exposure
