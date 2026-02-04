---
id: 0002
title: modern-dashboard-forest-neon-plan
stage: plan
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: 005-modern-dashboard-redesign
branch: 005-modern-dashboard-redesign
user: Sunaina Ismail
command: /sp.plan
labels: ["ui-redesign", "forest-neon-theme", "dashboard", "framer-motion", "recharts", "shadcn-ui"]
links:
  spec: ../spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-modern-dashboard-redesign/plan.md
  - specs/005-modern-dashboard-redesign/research.md
  - specs/005-modern-dashboard-redesign/data-model.md
  - specs/005-modern-dashboard-redesign/quickstart.md
  - specs/005-modern-dashboard-redesign/contracts/dashboard-api.md
  - specs/005-modern-dashboard-redesign/contracts/chart-data.md
  - specs/005-modern-dashboard-redesign/contracts/sidebar-state.md
  - CLAUDE.md (updated with new technologies)
tests:
  - none (planning phase)
---

## Prompt

# Project Specification: Todo App UI Redesign (Forest & Neon Edition)

## **Core Objective**
Implement a comprehensive UI redesign for the Todo application using Next.js 16 App Router, Framer Motion, shadcn/ui, and Recharts. The aesthetic must strictly follow a **High-Contrast Dark Emerald & Neon Lime** theme (inspired by the Forest Night dashboard style).

## **Technical Context & Architecture**
- **Framework:** Next.js 16 with App Router (use `/vercel/next.js/v16.1.1` documentation via Context7).
- **Type Safety:** Full TypeScript implementation for all components and props.
- **Rendering:** Server Components for initial page loads; Client Components for interactivity.
- **Loading Pattern:** Mandatory use of `loading.tsx` files for all routes.
- **Error Handling:** Implement proper error boundaries with `error.tsx` files and React Suspense.

## **UI & Animation Library**
- **Component Base:** shadcn/ui (use `/websites/ui_shadcn` via Context7).
  - *Required:* Sidebar, chart, card, skeleton, button, input, dialog, dropdown-menu.
- **Animations:** Framer Motion (use `/grx7/framer-motion` via Context7).
  - Layout animations for sidebar collapse/expand.
  - Page transition animations and stagger animations for list items.
  - Smooth enter/exit animations for modals and loading skeleton animations.
- **Responsive Strategy:**
  - **Mobile (< 768px):** Sidebar collapses to icons only or overlay.
  - **Tablet (768px - 1024px):** Sidebar toggleable.
  - **Desktop (> 1024px):** Sidebar expanded by default.

## **Color Scheme (The "Forest-Neon" Palette)**
**Strictly adhere to these HEX codes to match the design reference:**
- **Primary Background:** `#090E0C` (Forest Black) - Main canvas.
- **Surface/Cards:** `#111814` (Emerald Charcoal) - Sidebar, panels, and cards.
- **Primary Accent:** `#BEF264` (Neon Lime) - **All primary buttons**, active states, and highlights.
- **Text (Primary):** `#FFFFFF` (Pure White).
- **Text (Muted):** `#64748B` (Emerald-Gray) - For secondary labels.
- **Success:** `#10B981` (Emerald-500).
- **Warning:** `#F59E0B` (Amber-500).
- **Error:** `#EF4444` (Red-500).

## **Key Feature Implementation**

### **1. Sidebar Behavior**
- Desktop: Expanded by default, collapsible with smooth Framer Motion transitions.
- Mobile: Collapsed to icons only; expands as an overlay on tap.
- Active State: Use a "pill-shaped" background in **Neon Lime (#BEF264)** with black text.
- Persistence: Store collapse state in `localStorage`.

### **2. Charts & Data Viz (Recharts)**
- Use `ResponsiveContainer` for all charts.
- **Line/Area Charts:** Neon Lime strokes with a 10% opacity green gradient fill.
- **Donut Charts:** Neon Lime for completion segments; `#1A221E` for empty tracks.
- Implementation: Show axes first, then animate data (Progressive loading).

### **3. AI Chatbot (ChatKit)**
- Research React components at `.claude/skills/openai-chatkit-frontend-embed-skill/templates/`.
- Floating chat button in **Neon Lime (#BEF264)** accessible from all pages.
- Integrate with existing Phase 3 backend with smooth slide-in/out animations.

## **Implementation Requirements**
- **Documentation:** Use Context7 MCP to search documentation before implementing each feature.
- **Reusable Variants:** Create reusable Framer Motion animation variants for consistent motion design.
- **Optimization:** Use Next.js `Image` component and optimize all assets.
- **State Management:** Use Optimistic UI updates for mutations (task additions/deletions).

## **Research Tasks**
- Query Context7 for Next.js 16 App Router best practices for loading states.
- Query Context7 for Framer Motion sidebar collapse animation patterns.
- Query Context7 for shadcn/ui sidebar component implementation.
- Query Context7 for Recharts responsive chart examples.

## **Pages to Redesign**
1. `/sign-in` - Modern login form with animated Forest Black background.
2. `/sign-up` - Registration form with step indicators.
3. `/dashboard` - Overview with high-contrast charts and stats cards.
4. `/dashboard/tasks` - Task list with filters and Neon Lime interactive elements.
5. `/dashboard/tags` - Tag management interface.
6. `/dashboard/settings` - User settings and preferences.

## Response snapshot

Created comprehensive implementation plan for modern dashboard UI redesign with Forest & Neon color scheme. Completed all planning phases:

**Phase 0 - Research (Complete)**:
- Researched Next.js 16 App Router loading patterns via Context7
- Researched Framer Motion layout animations via Context7
- Researched shadcn/ui component integration via Context7
- Researched Recharts responsive patterns via Context7
- Reviewed ChatKit React templates locally
- Documented localStorage sidebar state persistence patterns
- Created research.md with all findings and implementation patterns

**Phase 1 - Design & Contracts (Complete)**:
- Created data-model.md defining 9 core entities (DashboardMetrics, ChartDataPoint, SidebarState, etc.)
- Created API contracts for dashboard metrics and chart data endpoints
- Created client-side contract for sidebar state persistence
- Created quickstart.md with step-by-step setup instructions
- Updated CLAUDE.md agent context with new technologies

**Planning Artifacts Created**:
- plan.md (439 lines) - Complete implementation plan with Forest & Neon theme specifications
- research.md (350+ lines) - Technology validation and implementation patterns
- data-model.md (300+ lines) - Data structures and type definitions
- quickstart.md (400+ lines) - Developer setup guide
- contracts/dashboard-api.md - Dashboard metrics endpoint contract
- contracts/chart-data.md - Chart data endpoints contract
- contracts/sidebar-state.md - Client-side state management contract

**Key Technical Decisions**:
- Next.js 16 App Router with loading.tsx files for all routes
- Framer Motion layout animations for sidebar (300ms transitions)
- shadcn/ui components with Forest & Neon CSS variable theme
- Recharts with custom Neon Lime gradients and responsive containers
- localStorage for sidebar state with SSR-safe hydration
- ChatKit integration with floating Neon Lime button

**Forest & Neon Theme Configuration**:
- Primary Background: #090E0C (Forest Black)
- Surface/Cards: #111814 (Emerald Charcoal)
- Primary Accent: #BEF264 (Neon Lime)
- All colors mapped to Tailwind CSS variables
- Custom gradient definitions for charts

**Constitutional Compliance**: All gates passed with justified complexity for UI dependencies

## Outcome

- ✅ Impact: Complete implementation plan with Forest & Neon theme, covering all 5 user stories (P1-P5), 6 research tasks, 9 data entities, 3 API contracts, and comprehensive quickstart guide
- 🧪 Tests: No tests at planning phase - test strategy defined in plan for component, integration, and E2E testing
- 📁 Files: Created 8 planning artifacts (plan.md, research.md, data-model.md, quickstart.md, 3 contracts, updated CLAUDE.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks organized by priority (P1-P5), then `/sp.implement` to execute
- 🧠 Reflection: Successfully translated user's Forest & Neon design vision into actionable technical plan. Research phase validated all technology choices via Context7. Data model and contracts provide clear implementation boundaries. Quickstart guide enables rapid developer onboarding.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all artifacts generated
- Graders run and results (PASS/FAIL): Constitutional Check - ALL PASS (Specification-First, Technology Constraints, Type Safety, Error Handling, Testing, Complexity Justification)
- Prompt variant (if applicable): Standard sp.plan workflow with detailed Forest & Neon theme specifications
- Next experiment (smallest change to try): Proceed to task generation phase to break down implementation into atomic, testable tasks aligned with user story priorities
