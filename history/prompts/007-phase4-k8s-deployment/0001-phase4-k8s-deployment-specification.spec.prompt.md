---
id: 0001
title: Phase4 K8s Deployment Specification
stage: spec
date: 2026-02-05
surface: agent
model: claude-haiku-4-5-20251001
feature: 007-phase4-k8s-deployment
branch: 007-phase4-k8s-deployment
user: sunaina_ubuntu
command: /sp.specify
labels: ["phase-4", "kubernetes", "minikube", "helm", "deployment", "specification", "health-probes", "configmaps", "secrets"]
links:
  spec: specs/007-phase4-k8s-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-phase4-k8s-deployment/spec.md
  - specs/007-phase4-k8s-deployment/checklists/requirements.md
tests:
  - None (specification phase)
---

## Prompt

Deploy Phase 3 AI-powered Todo application (FastAPI backend with OpenAI Agents SDK + Next.js ChatKit frontend) to local Minikube Kubernetes cluster with production-ready infrastructure.

User Journeys:
- Deploy entire application stack to Minikube using single automated command
- Access frontend via kubectl port-forward and NodePort service on port 30300
- Backend communicates internally via ClusterIP on port 8001
- Kubernetes automatically detects and restarts failed pods using health probes
- Manage configuration via ConfigMaps and secrets via Kubernetes Secrets
- Use AI-assisted DevOps tools (kubectl-ai, kagent, Docker AI/Gordon) for cluster operations
- Scale frontend and backend pods independently
- All Phase 3 features work without regression (auth, tasks, AI chatbot)

Acceptance Criteria:
- Helm 3.x charts package deployment with values.yaml and values-dev.yaml
- Frontend pods expose NodePort 30300, backend pods use ClusterIP port 8001
- Liveness probes (/api/health) and readiness probes (/api/ready) on all pods
- Frontend readiness validates environment variables, backend readiness tests database connection
- ConfigMaps store non-sensitive config, Secrets store DATABASE_URL, BETTER_AUTH_SECRET, API keys
- Container images build within Minikube using eval $(minikube docker-env)
- Single deployment script provisions stack in under 10 minutes
- Pods achieve Ready status within 120 seconds, respond within 5 seconds
- Failed pods restart within 30 seconds via liveness probe detection
- No secrets exposed in logs or pod environments
- External dependencies: Neon PostgreSQL database, Cloudflare R2 storage
- All pods stateless with no persistent volumes
- Port forwarding works: kubectl port-forward svc/frontend 3000:3000
- Documentation includes working kubectl-ai, kagent, and Docker AI examples

Success Metrics:
- 100% Phase 3 feature parity (no regression)
- Deployment completes in under 10 minutes
- Pods ready within 120 seconds
- Automatic pod recovery within 30 seconds
- Zero secret exposure in logs
- Horizontal scaling functional for both services

## Response snapshot

Successfully created comprehensive Phase 4 Kubernetes deployment specification with 7 prioritized user stories, 67 functional requirements, 12 measurable success criteria, and 10 edge cases.

**Branch Created**: 007-phase4-k8s-deployment

**Specification Structure**:
- **User Story 1 (P1)**: Automated Single-Command Deployment - Foundation for all other features
- **User Story 2 (P2)**: Health Monitoring and Auto-Recovery - Production readiness with liveness/readiness probes
- **User Story 3 (P3)**: Secure Configuration Management - ConfigMaps and Secrets with no plaintext exposure
- **User Story 4 (P4)**: Network Access and Service Exposure - Port-forward and NodePort/ClusterIP services
- **User Story 5 (P5)**: Horizontal Pod Scaling - Independent scaling for frontend and backend
- **User Story 6 (P6)**: AI-Assisted DevOps Documentation - kubectl-ai, kagent, Docker AI examples
- **User Story 7 (P7)**: Phase 3 Feature Parity - Zero regression requirement

**Functional Requirements** (67 total):
- Deployment Infrastructure (FR-001 to FR-013): Minikube, Helm, automated script
- Network Services (FR-014 to FR-018): NodePort 30300, ClusterIP 8001, port-forward
- Health Monitoring (FR-019 to FR-025): Liveness and readiness probes with configurable timing
- Configuration Management (FR-026 to FR-031): Secrets and ConfigMaps with security validation
- Container Images (FR-032 to FR-036): Multi-stage builds, non-root, resource limits
- Helm Charts (FR-037 to FR-045): Complete chart structure with values files
- Scalability (FR-046 to FR-050): Stateless pods, horizontal scaling
- External Dependencies (FR-051 to FR-054): Neon database, Cloudflare R2
- Performance (FR-055 to FR-057): 120s pod readiness, 5s response time
- Phase 3 Feature Parity (FR-058 to FR-061): Zero regression validation
- Documentation (FR-062 to FR-067): AI DevOps tool examples and troubleshooting

**Success Criteria** (12 measurable outcomes):
- All technology-agnostic and verifiable
- Time-bound metrics (10min deployment, 120s readiness, 30s recovery, 5s response)
- Quality metrics (100% feature parity, zero secret exposure)
- Scalability validation (independent pod scaling)

**Quality Validation**: ✅ PASSED
- All checklist items passed
- No [NEEDS CLARIFICATION] markers
- Requirements are testable and unambiguous
- Ready for planning phase

## Outcome

- ✅ Impact: Complete Phase 4 Kubernetes deployment specification created with constitutional compliance. All Phase IV mandatory requirements addressed including Minikube, Helm, health probes, ConfigMaps/Secrets, NodePort/ClusterIP, automated deployment, and AI DevOps documentation.
- 🧪 Tests: None (specification phase - tests will be defined in tasks phase)
- 📁 Files: 2 files created (spec.md with 282 lines, checklists/requirements.md)
- 🔁 Next prompts: Run `/sp.plan` to generate implementation plan with technical architecture, research decisions, and data models. Then `/sp.tasks` to break down into actionable tasks.
- 🧠 Reflection: Specification is comprehensive and production-ready. Backend port changed to 8001 per user requirement (8000 already in use). Port forwarding approach included as requested from reference code. All 7 user stories are independently testable with clear priorities. Edge cases cover common Kubernetes failure scenarios. Success criteria are measurable and technology-agnostic. Ready to proceed with planning phase.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification completed successfully with all quality checks passed
- Graders run and results (PASS/FAIL): PASS - All 14 checklist items validated successfully, no [NEEDS CLARIFICATION] markers, all requirements testable
- Prompt variant (if applicable): Standard /sp.specify workflow with comprehensive user input
- Next experiment (smallest change to try): Proceed with /sp.plan to generate technical implementation plan including Dockerfile updates, Helm chart structure, deployment script design, and health endpoint implementation
