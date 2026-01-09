# Tasks: Next.js 16 Todo Frontend

**Input**: Design documents from `/specs/003-todo-frontend/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, quickstart.md

**Tests**: Not explicitly requested - omitting test tasks per spec requirements

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Frontend project: `phase-2-todo-full-stack/frontend/`
- Components: `phase-2-todo-full-stack/frontend/components/`
- Server Actions: `phase-2-todo-full-stack/frontend/actions/`
- Types: `phase-2-todo-full-stack/frontend/types/`
- Lib: `phase-2-todo-full-stack/frontend/lib/`
- Tests: `phase-2-todo-full-stack/frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per implementation plan in phase-2-todo-full-stack/frontend/
- [X] T002 Initialize Next.js 16 project with TypeScript using `npx create-next-app@latest`
- [X] T003 [P] Install dependencies: better-auth, jose, date-fns, clsx, tailwind-merge
- [X] T004 [P] Install and configure Shadcn UI components (button, input, dialog, etc.)
- [X] T005 [P] Configure ESLint and Prettier for consistent code formatting
- [X] T006 [P] Configure tailwind.config.js with custom theme settings
- [X] T007 Create .env.local with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_APP_URL
- [X] T008 Update tsconfig.json for strict mode and path aliases

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 Create TypeScript types in phase-2-todo-full-stack/frontend/types/task.ts (Task, TaskCreate, TaskUpdate interfaces)
- [X] T010 [P] Create TypeScript types in phase-2-todo-full-stack/frontend/types/filters.ts (TaskFilters, PaginationMeta, TaskListResponse)
- [X] T011 [P] Create TypeScript types in phase-2-todo-full-stack/frontend/types/auth.ts (SignUpForm, SignInForm, UserSession)
- [X] T012 [P] Create TypeScript types in phase-2-todo-full-stack/frontend/types/api.ts (API request/response types)
- [X] T013 Implement API client in phase-2-todo-full-stack/frontend/lib/api-client.ts with JWT token attachment
- [X] T014 [P] Configure Better Auth in phase-2-todo-full-stack/frontend/lib/auth-client.ts with JWT adapter
- [X] T015 [P] Create utility functions in phase-2-todo-full-stack/frontend/lib/utils.ts (cn helper, date formatters)
- [X] T016 [P] Setup Shadcn UI base components in phase-2-todo-full-stack/frontend/components/ui/ (Button, Input, Dialog, Label, Select, Card, Badge, Skeleton, Toast)
- [X] T017 Create root layout in phase-2-todo-full-stack/frontend/app/layout.tsx with providers
- [X] T018 Create home page redirect logic in phase-2-todo-full-stack/frontend/app/page.tsx (redirect to dashboard if authenticated)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) MVP

**Goal**: Users can sign up, sign in, and sign out securely

**Independent Test**: A new user can complete sign-up flow, receive confirmation, and access the dashboard

- [X] T019 [P] [US1] Create sign-up page in phase-2-todo-full-stack/frontend/app/(auth)/sign-up/page.tsx
- [X] T020 [P] [US1] Create sign-up form component in phase-2-todo-full-stack/frontend/components/auth/sign-up-form.tsx
- [X] T021 [P] [US1] Create sign-in page in phase-2-todo-full-stack/frontend/app/(auth)/sign-in/page.tsx
- [X] T022 [P] [US1] Create sign-in form component in phase-2-todo-full-stack/frontend/components/auth/sign-in-form.tsx
- [X] T023 [US1] Create auth server actions in phase-2-todo-full-stack/frontend/actions/auth.ts (signUp, signIn, signOut)
- [X] T024 [US1] Create Better Auth API handler in phase-2-todo-full-stack/frontend/app/api/auth/[...all]/route.ts
- [X] T025 [US1] Create auth layout in phase-2-todo-full-stack/frontend/app/(auth)/layout.tsx
- [X] T026 [US1] Implement session protection middleware for dashboard routes (proxy.ts in Next.js 16)
- [X] T027 [US1] Add form validation for email/password fields

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1) MVP

**Goal**: Authenticated users can see all their tasks in a list with proper loading and error states

**Independent Test**: User sees their tasks rendered from the FastAPI backend with proper loading states and error handling

- [X] T028 [P] [US2] Create dashboard layout in phase-2-todo-full-stack/frontend/app/dashboard/layout.tsx with header/sidebar
- [X] T029 [P] [US2] Create header component in phase-2-todo-full-stack/frontend/components/layout/header.tsx with user menu
- [X] T030 [P] [US2] Create user menu component in phase-2-todo-full-stack/frontend/components/layout/user-menu.tsx with sign-out
- [X] T031 [US2] Create dashboard page in phase-2-todo-full-stack/frontend/app/dashboard/page.tsx
- [X] T032 [P] [US2] Create task list component in phase-2-todo-full-stack/frontend/components/tasks/task-list.tsx
- [X] T033 [P] [US2] Create task item component in phase-2-todo-full-stack/frontend/components/tasks/task-item.tsx (displays title, completion, priority, tags)
- [X] T034 [US2] Create empty state component in phase-2-todo-full-stack/frontend/components/tasks/task-empty.tsx
- [X] T035 [P] [US2] Create loading skeleton component in phase-2-todo-full-stack/frontend/components/tasks/task-skeleton.tsx
- [X] T036 [US2] Create task fetch server action in phase-2-todo-full-stack/frontend/actions/tasks.ts (getTasks)
- [X] T037 [US2] Add error boundary and retry mechanism for task loading

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Create Task (Priority: P1) MVP

**Goal**: Users can create new tasks with title, description, priority, due date, and tags

**Independent Test**: User can fill out a task form with all fields and see the new task appear in their list

- [X] T038 [P] [US3] Create task form component in phase-2-todo-full-stack/frontend/components/tasks/task-form.tsx
- [X] T039 [P] [US3] Create title input in phase-2-todo-full-stack/frontend/components/tasks/task-form.tsx with validation
- [X] T040 [P] [US3] Create description textarea in phase-2-todo-full-stack/frontend/components/tasks/task-form.tsx
- [X] T041 [P] [US3] Create priority select in phase-2-todo-full-stack/frontend/components/tasks/task-form.tsx (High/Medium/Low)
- [X] T042 [P] [US3] Create due date picker in phase-2-todo-full-stack/frontend/components/tasks/task-form.tsx
- [X] T043 [US3] Create tag input in phase-2-todo-full-stack/frontend/components/tasks/task-form.tsx (comma-separated)
- [X] T044 [P] [US3] Create "Add Task" button in phase-2-todo-full-stack/frontend/components/tasks/add-task-button.tsx
- [X] T045 [US3] Create task dialog/modal in phase-2-todo-full-stack/frontend/components/tasks/task-dialog.tsx
- [X] T046 [US3] Implement createTask server action in phase-2-todo-full-stack/frontend/actions/tasks.ts
- [X] T047 [US3] Add optimistic UI update after task creation
- [X] T048 [US3] Add form validation (title required, max lengths)

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently

---

## Phase 6: User Story 4 - Toggle Task Completion (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete with immediate visual feedback

**Independent Test**: User can click a checkbox to toggle task completion and see the visual state change immediately

- [X] T049 [P] [US4] Create checkbox component in phase-2-todo-full-stack/frontend/components/tasks/task-checkbox.tsx
- [X] T050 [US4] Implement toggleComplete server action in phase-2-todo-full-stack/frontend/actions/tasks.ts
- [X] T051 [US4] Add optimistic UI update for toggle action
- [X] T052 [US4] Add error handling with revert on failure
- [X] T053 [P] [US4] Update task-item.tsx to include checkbox with toggle functionality

**Checkpoint**: User Story 4 complete - can work in parallel with US5-US8

---

## Phase 7: User Story 5 - Edit Task (Priority: P2)

**Goal**: Users can edit task details to update or correct their tasks

**Independent Test**: User can open a task in edit mode, modify any field, and save changes

- [X] T054 [P] [US5] Create edit task form in phase-2-todo-full-stack/frontend/components/tasks/edit-task-form.tsx
- [X] T055 [US5] Pre-fill edit form with current task values
- [X] T056 [US5] Create edit mode toggle in phase-2-todo-full-stack/frontend/components/tasks/task-item.tsx
- [X] T057 [US5] Implement updateTask server action in phase-2-todo-full-stack/frontend/actions/tasks.ts
- [X] T058 [US5] Add form validation (title required on save)
- [X] T059 [US5] Add optimistic UI update for task edits
- [X] T060 [US5] Add edit/cancel button handling

**Checkpoint**: User Story 5 complete - can work in parallel with US4, US6-US8

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks with confirmation to remove items they no longer need

**Independent Test**: User can delete a task with confirmation, and the task disappears from the list

- [X] T061 [P] [US6] Create delete confirmation dialog in phase-2-todo-full-stack/frontend/components/tasks/delete-dialog.tsx
- [X] T062 [US6] Create delete button in phase-2-todo-full-stack/frontend/components/tasks/task-item.tsx
- [X] T063 [US6] Implement deleteTask server action in phase-2-todo-full-stack/frontend/actions/tasks.ts
- [X] T064 [US6] Add optimistic UI removal on confirmation
- [X] T065 [US6] Add cancel button handling to keep task unchanged

**Checkpoint**: User Story 6 complete - can work in parallel with US4, US5, US7, US8

---

## Phase 9: User Story 7 - Search and Filter Tasks (Priority: P2)

**Goal**: Users with many tasks can search, filter, sort, and paginate to find specific tasks

**Independent Test**: User can search text, filter by priority/tags, sort by different fields, and see paginated results

- [X] T066 [P] [US7] Create search input component in phase-2-todo-full-stack/frontend/components/tasks/search-input.tsx
- [X] T067 [P] [US7] Create priority filter component in phase-2-todo-full-stack/frontend/components/tasks/priority-filter.tsx
- [X] T068 [P] [US7] Create tag filter component in phase-2-todo-full-stack/frontend/components/tasks/tag-filter.tsx
- [X] T069 [P] [US7] Create sort controls component in phase-2-todo-full-stack/frontend/components/tasks/sort-controls.tsx
- [X] T070 [P] [US7] Create pagination controls in phase-2-todo-full-stack/frontend/components/tasks/pagination-controls.tsx
- [X] T071 [US7] Implement filterTasks server action in phase-2-todo-full-stack/frontend/actions/tasks.ts
- [X] T072 [US7] Update task list component to accept filter props
- [X] T073 [US7] Add debounce for search input (500ms delay)
- [X] T074 [US7] Persist filter state in URL query parameters

**Checkpoint**: User Story 7 complete - can work in parallel with US4-US6, US8

---

## Phase 10: User Story 8 - View Tags (Priority: P2)

**Goal**: Users can see all their tags with usage counts for organization

**Independent Test**: User can see a list of all their tags sorted alphabetically with task counts

- [X] T075 [P] [US8] Create tag list component in phase-2-todo-full-stack/frontend/components/tasks/tag-list.tsx
- [X] T076 [P] [US8] Create tag item component in phase-2-todo-full-stack/frontend/components/tasks/tag-item.tsx with usage count
- [X] T077 [US8] Create empty tag state in phase-2-todo-full-stack/frontend/components/tasks/tag-empty.tsx
- [X] T078 [US8] Implement getTags server action in phase-2-todo-full-stack/frontend/actions/tasks.ts
- [X] T079 [US8] Integrate tag list into dashboard sidebar or header
- [X] T080 [US8] Add click-to-filter functionality for tags

**Checkpoint**: User Story 8 complete - all user stories now independently functional

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T081 [P] Implement responsive design for mobile (320px+) and desktop (1200px+)
- [X] T082 [P] Add loading states and skeleton screens for all async operations
- [X] T083 [P] Implement error handling with toast notifications and retry options
- [X] T084 [P] Add keyboard navigation and accessibility (ARIA labels, focus management)
- [X] T085 [P] Optimize performance (lazy loading, memoization, debounced search)
- [X] T086 [P] Add date-fns formatting for due dates and timestamps
- [X] T087 [P] Final type checking with `npm run type-check`
- [X] T088 [P] Run linting with `npm run lint` and fix all issues
- [ ] T089 [P] Verify all success criteria from spec.md (SC-001 through SC-009)
- [ ] T090 [P] Run quickstart.md validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

| Story | Priority | Can Start After | Dependencies |
|-------|----------|-----------------|--------------|
| US1 | P1 | Foundational (T009-T018) | None - do first |
| US2 | P1 | Foundational (T009-T018) | US1 recommended (auth) |
| US3 | P1 | Foundational (T009-T018) | US1 required (auth context) |
| US4 | P2 | Foundational (T009-T018) | US2-US3 (list, create) |
| US5 | P2 | Foundational (T009-T018) | US2-US3 (list, create) |
| US6 | P3 | Foundational (T009-T018) | US2-US3 (list, create) |
| US7 | P2 | Foundational (T009-T018) | US2 (task list) |
| US8 | P2 | Foundational (T009-T018) | US3 (task creation with tags) |

### Within Each User Story

- Models/types before components
- Components before server actions
- Server actions before integration
- Story complete before moving to next priority

---

## Parallel Opportunities

### Phase 1 (Setup) - All tasks can run in parallel:
```bash
Task T003: Install dependencies
Task T004: Configure Shadcn UI
Task T005: Configure ESLint/Prettier
Task T006: Configure Tailwind
Task T007: Create .env.local
```

### Phase 2 (Foundational) - Parallel within limits:
```bash
Task T010: Create types/filters.ts
Task T011: Create types/auth.ts
Task T012: Create types/api.ts
Task T014: Configure Better Auth
Task T015: Create utils.ts
Task T016: Setup Shadcn UI components
```

### Phase 3-10 (User Stories) - All can run in parallel after Foundational:
With multiple developers, each can work on a different user story:
- Developer A: US1 (Auth)
- Developer B: US2 (View Tasks)
- Developer C: US3 (Create Task)
- Developer D: US4-US8 (remaining stories)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Auth)
4. **STOP and VALIDATE**: Test auth flow works
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → Test → Deploy (Auth working!)
3. Add US2 → Test → Deploy (View tasks!)
4. Add US3 → Test → Deploy (Create tasks!)
5. Add US4-US8 → Test → Deploy (Complete app!)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (Auth)
   - Developer B: US2 + US3 (Task list + Create)
   - Developer C: US4 + US5 + US6 (Task actions)
   - Developer D: US7 + US8 (Search + Tags)

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 90 |
| Phase 1 (Setup) | 8 tasks |
| Phase 2 (Foundational) | 10 tasks |
| Phase 3 (US1 - Auth) | 9 tasks |
| Phase 4 (US2 - View Tasks) | 10 tasks |
| Phase 5 (US3 - Create Task) | 11 tasks |
| Phase 6 (US4 - Toggle) | 5 tasks |
| Phase 7 (US5 - Edit) | 7 tasks |
| Phase 8 (US6 - Delete) | 5 tasks |
| Phase 9 (US7 - Search/Filter) | 9 tasks |
| Phase 10 (US8 - View Tags) | 6 tasks |
| Phase 11 (Polish) | 10 tasks |

| User Story | Tasks | Priority |
|------------|-------|----------|
| US1: Authentication | 9 | P1 (MVP) |
| US2: View Tasks | 10 | P1 (MVP) |
| US3: Create Task | 11 | P1 (MVP) |
| US4: Toggle Completion | 5 | P2 |
| US5: Edit Task | 7 | P2 |
| US6: Delete Task | 5 | P3 |
| US7: Search/Filter | 9 | P2 |
| US8: View Tags | 6 | P2 |

**MVP Scope**: Phases 1-5 (US1-US3) = 48 tasks = 53% of total

**Parallel Opportunities**: 35+ tasks marked [P] can run concurrently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Verify success criteria SC-001 through SC-009 from spec.md
