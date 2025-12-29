---
description: "Task list for Todo In-Memory Python Console App implementation"
---

# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/
- [X] T002 Initialize Python project with rich dependencies in requirements.txt
- [X] T003 [P] Configure linting and formatting tools (mypy, black, flake8)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create TaskStatus enum in src/models/task.py
- [X] T005 [P] Create Task model with validation in src/models/task.py
- [X] T006 Create TaskRepository interface in src/repositories/task_repository.py
- [X] T007 Implement in-memory TaskRepository with CRUD operations in src/repositories/task_repository.py
- [X] T008 Create TaskService with business logic in src/services/task_service.py
- [X] T009 Create UI helper functions in src/cli/ui.py
- [X] T010 Create basic console menu structure in src/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their to-do list with a mandatory title and optional description, assigning a unique ID and setting status to pending by default

**Independent Test**: Can be fully tested by adding a new task with a title and verifying it appears in the task list with a unique ID and pending status

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement Task creation validation in src/models/task.py
- [X] T012 [US1] Implement create_task method in src/repositories/task_repository.py
- [X] T013 [US1] Implement create_task method in src/services/task_service.py
- [X] T014 [US1] Add create task functionality to console menu in src/cli/main.py
- [X] T015 [US1] Add input validation and error handling for task creation in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display all tasks in a clear, organized format so users can understand their current workload and priorities

**Independent Test**: Can be fully tested by creating several tasks and then viewing the complete list to verify proper display formatting and sorting

### Implementation for User Story 2

- [X] T016 [P] [US2] Implement get_all_tasks method in src/repositories/task_repository.py
- [X] T017 [US2] Implement get_all_tasks method in src/services/task_service.py
- [X] T018 [US2] Create rich table formatting for task display in src/cli/ui.py
- [X] T019 [US2] Add view tasks functionality to console menu in src/cli/main.py
- [X] T020 [US2] Implement proper sorting by ID and "No tasks available" message in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Toggle Task Completion (Priority: P2)

**Goal**: Allow users to mark tasks as completed or pending to track progress and distinguish between finished and unfinished work

**Independent Test**: Can be fully tested by toggling a task's status and verifying it changes from pending to completed or vice versa

### Implementation for User Story 3

- [X] T021 [P] [US3] Implement toggle_task_status method in src/repositories/task_repository.py
- [X] T022 [US3] Implement toggle_task_status method in src/services/task_service.py
- [X] T023 [US3] Add toggle task functionality to console menu in src/cli/main.py
- [X] T024 [US3] Add validation for task ID existence and error handling in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Edit Task (Priority: P2)

**Goal**: Allow users to modify the title or description of their tasks so they can update details as needed

**Independent Test**: Can be fully tested by editing a task's details and verifying the changes are reflected in the system

### Implementation for User Story 4

- [X] T025 [P] [US4] Implement update_task method in src/repositories/task_repository.py
- [X] T026 [US4] Implement update_task method in src/services/task_service.py
- [X] T027 [US4] Add edit task functionality to console menu in src/cli/main.py
- [X] T028 [US4] Add validation for task ID existence and input validation in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Remove Task (Priority: P3)

**Goal**: Allow users to delete tasks that are no longer needed so their task list remains manageable and relevant

**Independent Test**: Can be fully tested by removing a task and verifying it no longer appears in the task list

### Implementation for User Story 5

- [X] T029 [P] [US5] Implement delete_task method in src/repositories/task_repository.py
- [X] T030 [US5] Implement delete_task method in src/services/task_service.py
- [X] T031 [US5] Add delete task functionality to console menu in src/cli/main.py
- [X] T032 [US5] Add validation for task ID existence and error handling in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T033 [P] Add comprehensive error handling across all layers in src/
- [X] T034 [P] Add timestamp update functionality when tasks are modified in src/models/task.py
- [X] T035 Add input validation for special characters and emojis as per spec in src/models/task.py
- [X] T036 [P] Update UI to show green checkmark indicators for completed tasks in src/cli/ui.py
- [X] T037 [P] Add proper ISO 8601 timestamp formatting in src/models/task.py
- [X] T038 Run type checking with mypy --strict on src/ directory
- [X] T039 Test complete application flow with all user stories integrated
- [X] T040 Update README.md with usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - May integrate with other stories but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints/UI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all foundational components together:
Task: "Create TaskStatus enum in src/models/task.py"
Task: "Create Task model with validation in src/models/task.py"

# Launch all US1 implementation tasks together:
Task: "Implement Task creation validation in src/models/task.py"
Task: "Implement create_task method in src/repositories/task_repository.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1-2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Create Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence