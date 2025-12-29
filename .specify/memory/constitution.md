<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified sections: Quality & Verification Gates (expanded with Automated Testing + AI Sub-Agents), Technology Constraints (Phase II details clarified)
- Added gates: Automated Testing, AI Sub-Agents and Skills
- Removed sections: None
- Templates requiring updates: ✅ All templates already align with constitution
- Follow-up TODOs: None
-->
# Hackathon II Todo Constitution

## Core Principles

### Foundational Philosophy (SDD-RI)
**Specification-First Discipline**: No implementation is permitted without a corresponding specification. Mandatory workflow sequence: *Constitution → Specification → Plan → Tasks → Implementation*. **AI-Driven Development**: Humans operate as Architects and Reviewers only. All code must be generated exclusively through **Spec-Kit Plus**. **Intelligence Over Artifacts**: The system prioritizes reusable cognitive assets (ADRs, PHRs, reusable reasoning units) over manual coding. Code is disposable; intelligence is permanent.

### Architectural Doctrine
**Evolution-Ready Design**: Each phase must prepare the foundations for future functionality, enabling components to be replaced or upgraded without breaking contracts. **Separation of Concerns**: Business logic decoupled from presentation and interfaces; Storage abstracted behind clear boundaries; No hidden side-effects or cross-layer leakage. **Human-Centered Interaction**: All interfaces must be predictable, forgiving, and helpful, with clear guidance and consistent error messaging.

### Execution & Workflow Standards
**Checkpoint Protocol**: Work is performed in atomic cycles — *Generate → Review → Commit → Proceed*. No partial merges or speculative changes. **Test-Defined Behavior**: Behavioral tests, edge cases, and expected outputs must be embedded in the specification prior to any implementation. **Versioned Knowledge System**: Every specification and architectural decision is versioned to preserve historical reasoning and project evolution.

### Technology Constraints
**Mandatory Technologies**: Python 3.13+, uv, TypeScript, FastAPI, SQLModel, Next.js, Tailwind CSS, Neon PostgreSQL, Better Auth (JWT), OpenAI Agents SDK, MCP, Docker, Kubernetes, Kafka, Dapr. **Phase-Specific Requirements**: Phase I requires Python console app with in-memory storage; Phase II requires Next.js 16+ frontend with FastAPI backend, SQLModel ORM, Neon PostgreSQL database, and Better Auth with JWT authentication; Phase III requires OpenAI ChatKit, Agents SDK, and MCP; Phase IV requires Minikube, Helm, kubectl-ai, and Kagent; Phase V requires Kafka, Dapr, and cloud deployment (DigitalOcean, GKE, or AKS). **Forbidden Technologies**: No unapproved technologies beyond the specified stack are permitted.

### Quality & Verification Gates
**Type Safety Enforcement**: Mandatory `mypy --strict` for Python and `tsc --strict` for TypeScript. **Explicit Error Handling**: No silent failures, hidden exceptions, or ambiguous states. All errors must be structured, descriptive, and actionable. **12-Factor Alignment**: Configuration, environment management, and future scalability must follow 12-factor methodology. **Code Quality**: No placeholder logic, dead code, or speculative features are allowed. **Automated Testing**: The project MUST include automated tests for both frontend and backend. Backend MUST include API integration tests for all endpoints. Backend tests MUST verify JWT authentication and user isolation. Frontend MUST include component tests and integration tests. All tests MUST pass before merging any changes. **AI Sub-Agents and Skills**: The project explicitly supports the use of multiple AI sub-agents and reusable skills, provided they strictly adhere to this constitution and the spec-driven workflow. Each sub-agent MUST have a clear, narrow role (e.g., writing specifications, planning, implementation, testing, or refactoring) and MUST NOT bypass the established specification or plan.

### Definition of Done
**Constitutional Compliance**: A feature, component, or phase is complete only when it adheres to all Constitutional rules without exception. **Specification Fulfillment**: It must precisely fulfill the approved Specification. **Build & Validation**: It must build, validate, and run without errors. **Reproducibility**: It must be fully regenerable from specifications in a reproducible manner.

## Architectural Standards
**Evolution-Ready Design**: Each phase must prepare foundations for future functionality, enabling components to be replaced or upgraded without breaking contracts. **Decoupling**: Business logic must be decoupled from presentation and interfaces; storage must be abstracted behind clear boundaries. **Error Handling**: All interfaces must implement structured, descriptive error handling with clear guidance and consistent messaging.

## Development Workflow
**Specification-First**: All implementation must be preceded by formal specification using Spec-Kit Plus. **AI-Driven Development**: All code generation must be performed exclusively through Claude Code and Spec-Kit Plus. **Checkpoint Protocol**: Work must follow atomic cycles: *Generate → Review → Commit → Proceed*. **Quality Gates**: All code must pass type safety checks, have explicit error handling, and align with 12-factor methodology.

## Governance
**Constitutional Authority**: This Constitution supersedes all other development practices and guidelines. **Amendment Process**: Changes to this Constitution require formal documentation and approval process. **Compliance Verification**: All pull requests and reviews must verify constitutional compliance. **Phase Progression**: Each phase must be completed before proceeding to the next phase.

**Version**: 1.1.0 | **Ratified**: 2025-12-08 | **Last Amended**: 2025-12-29
