---
id: 2
title: todo-in-memory-app-spec
stage: spec
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-app
branch: 001-todo-app
user: Sunaina Ismail
command: /sp.specify
labels: ["specification", "todo-app", "console-app"]
links:
  spec: /mnt/d/todo-hackathon/specs/001-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - /mnt/d/todo-hackathon/specs/001-todo-app/spec.md
 - /mnt/d/todo-hackathon/specs/001-todo-app/checklists/requirements.md
 - /mnt/d/todo-hackathon/.claude/commands/sp.specify.md
tests:
 - unit tests for task CRUD operations
 - validation tests for input constraints
 - UI flow tests for console menu
---

## Prompt

```text
# Todo In-Memory Python Console App Specification

## Overview
Build a Python console-based task manager with **in-memory storage**.
Follow **clean architecture**, strict **type hints**, and **repository pattern**.
No external database or persistent storage allowed.

---

## Features

### 1. Create New Task
- Inputs: `Title` (mandatory), `Description` (optional).
- Assigns unique numeric ID (auto-increment: `max(existing_ids)+1`).
- `created_at` timestamp auto-generated.
- Status defaults to `PENDING`.

### 2. View All Tasks
- Displays all tasks in **rich table format**.
- Columns: ID, Title, Description, Status, Created At, Last Updated.
- Completed tasks show **green checkmark**.
- Sorted ascending by ID.
- Empty list message: `"No tasks available"`.

### 3. Edit Task
- Modify Title and/or Description by **task ID**.
- Updates `updated_at` timestamp.
- Invalid ID → `"Task ID not found"`.

### 4. Remove Task
- Deletes a task by **task ID**.
- Updates in-memory list immediately.
- Invalid ID → `"Task ID not found"`.

### 5. Toggle Completion
- Switches task status between `PENDING` and `COMPLETED`.
- Input: task ID.
- Visual indicator: green checkmark for completed.
- Invalid ID → descriptive error.

---

## Business Logic

### Validation
- Title: non-empty, max length 100 characters.
- IDs must exist before edit/delete/toggle.

### State Management
- Tasks stored **in-memory in repository list**.
- All operations (add/edit/delete/toggle) **modify list atomically**.

### ID Management
- Unique integer IDs, auto-incremented.

### Status
- Enum: `PENDING` / `COMPLETED`.
- Toggle flips enum value.

### Display
- Use **rich tables**.
- Completed tasks include green checkmark.
- Messages are clear, concise, user-friendly.

---

## Architecture & Design

- **Repository Pattern**: `repository.py` handles all CRUD logic.
- **Service Layer**: `service.py` implements business rules.
- **CLI Layer**: `ui.py` handles user interaction.
- **Type Safety**: full `mypy` hints.
- **Testable**: unit tests cover all CRUD, toggle, and edge cases.

---

## CLI Flow
 # Todo Manager

1. Add New Task
2. View All Tasks
3. Edit Task
4. Delete Task
5. Toggle Completion
6. Exit

**Select an option:** _
- Invalid menu → `"Invalid option. Please try again."`

---

## Definition of Done
- All input validated and handled gracefully.
- In-memory repository reflects accurate state.
- CLI output is formatted and intuitive.
- Unit tests cover 100% of CRUD and toggle logic.
- Passes `mypy --strict` with no errors.
- Fully reproducible from this specification using **Spec-Kit Plus**.
```

## Response snapshot

Created comprehensive specification for the Todo In-Memory Python Console App with:

1. Detailed user stories with priorities (P1-P3) covering all required functionality
2. Acceptance scenarios for each user story
3. Edge case considerations
4. 17 functional requirements (FR-001 through FR-017) covering all specified features
5. Key entities definition (Task, TaskRepository, TaskService, TaskUI)
6. 6 measurable success criteria (SC-001 through SC-006)

The specification follows clean architecture principles, includes validation for all input constraints, and provides clear error handling requirements. All implementation details were avoided, focusing on user value and business needs.

## Outcome

- ✅ Impact: Complete feature specification created for todo console app with in-memory storage
- 🧪 Tests: Unit tests, validation tests, and UI flow tests planned
- 📁 Files: spec.md and requirements.md checklist created in specs/001-todo-app/
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification follows clean architecture and repository pattern as requested

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All checklist items validated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation planning with /sp.plan