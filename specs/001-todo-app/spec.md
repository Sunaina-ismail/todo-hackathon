# Feature Specification: Todo In-Memory Python Console App

**Feature Branch**: `001-todo-app`
**Created**: 2025-12-08
**Status**: Draft
**Input**: User description: "Build a Python console-based task manager with in-memory storage. Follow clean architecture, strict type hints, and repository pattern. No external database or persistent storage allowed."

## Clarifications

### Session 2025-12-08

- Q: Should the system accept special characters, emojis, or only alphanumeric characters in task titles? → A: Allow all printable Unicode characters including special characters and emojis
- Q: Should there be any character limit or content restrictions for task descriptions? → A: Allow up to 500 characters with printable Unicode including special characters and emojis
- Q: Should error messages be specific to the validation failure or more generic? → A: Specific error messages that clearly indicate what went wrong and how to fix it
- Q: Should timestamps be displayed in a specific format in the UI? → A: ISO 8601 format (YYYY-MM-DD HH:MM:SS)
- Q: Should task IDs be permanent or can they be reused after deletion? → A: IDs are permanent and never reused even after deletion

### Session 2025-12-09

- Q: What should the 6th menu option be since FR-001 specifies options 1-6 but only 5 operations are clearly defined? → A: The 6th menu option should be Exit to allow users to quit the application
- Q: How should the application handle errors to ensure stability? → A: Errors should be handled gracefully with user-friendly messages while allowing the application to continue running
- Q: When should data validation occur in the application? → A: Validate data on creation and update operations, but not on retrieval
- Q: How should console input be handled for optimal user experience? → A: Console input should be synchronous with immediate validation and feedback
- Q: Does the system need to handle concurrent access scenarios? → A: Single-user console app with no concurrent access needed

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Task (Priority: P1)

As a user, I want to add new tasks to my to-do list so that I can keep track of what I need to do. The system should accept a mandatory title and optional description, assign a unique ID, and set the status to pending by default.

**Why this priority**: This is the foundational feature that allows users to begin using the task manager. Without the ability to create tasks, other functionality is meaningless.

**Independent Test**: Can be fully tested by adding a new task with a title and verifying it appears in the task list with a unique ID and pending status.

**Acceptance Scenarios**:

1. **Given** I am at the main menu, **When** I select option 1 and enter a valid title, **Then** a new task is created with a unique ID, current timestamp, and pending status
2. **Given** I am creating a new task, **When** I enter a title with more than 100 characters, **Then** I receive an error message and the task is not created
3. **Given** I am creating a new task, **When** I enter an empty title, **Then** I receive an error message and the task is not created

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I want to see all my tasks displayed in a clear, organized format so that I can understand my current workload and priorities.

**Why this priority**: This is essential functionality that allows users to view and manage their tasks. Without this, users cannot effectively use the task manager.

**Independent Test**: Can be fully tested by creating several tasks and then viewing the complete list to verify proper display formatting and sorting.

**Acceptance Scenarios**:

1. **Given** I have multiple tasks in the system, **When** I select option 2, **Then** all tasks are displayed in a rich table format sorted by ID
2. **Given** I have no tasks in the system, **When** I select option 2, **Then** I see the message "No tasks available"
3. **Given** I have completed tasks, **When** I view the task list, **Then** completed tasks show a green checkmark indicator

---

### User Story 3 - Toggle Task Completion (Priority: P2)

As a user, I want to mark tasks as completed or pending so that I can track my progress and distinguish between finished and unfinished work.

**Why this priority**: This allows users to update the status of their tasks, which is a core function of a task manager.

**Independent Test**: Can be fully tested by toggling a task's status and verifying it changes from pending to completed or vice versa.

**Acceptance Scenarios**:

1. **Given** I have a pending task, **When** I select option 5 and enter the task ID, **Then** the task status changes to completed
2. **Given** I have a completed task, **When** I select option 5 and enter the task ID, **Then** the task status changes to pending
3. **Given** I enter an invalid task ID, **When** I try to toggle completion, **Then** I receive an error message "Task ID not found"

---

### User Story 4 - Edit Task (Priority: P2)

As a user, I want to modify the title or description of my tasks so that I can update details as needed.

**Why this priority**: This allows users to maintain accurate task information as requirements change.

**Independent Test**: Can be fully tested by editing a task's details and verifying the changes are reflected in the system.

**Acceptance Scenarios**:

1. **Given** I have an existing task, **When** I select option 3 and enter valid updates, **Then** the task details are updated with a new timestamp
2. **Given** I enter an invalid task ID, **When** I try to edit a task, **Then** I receive an error message "Task ID not found"
3. **Given** I enter a title with more than 100 characters, **When** I try to edit a task, **Then** I receive an error message and the task is not modified

---

### User Story 5 - Remove Task (Priority: P3)

As a user, I want to delete tasks that are no longer needed so that my task list remains manageable and relevant.

**Why this priority**: This allows users to clean up their task list by removing outdated or unnecessary tasks.

**Independent Test**: Can be fully tested by removing a task and verifying it no longer appears in the task list.

**Acceptance Scenarios**:

1. **Given** I have an existing task, **When** I select option 4 and enter the task ID, **Then** the task is removed from the system
2. **Given** I enter an invalid task ID, **When** I try to delete a task, **Then** I receive an error message "Task ID not found"

---

### Edge Cases

- What happens when trying to edit/delete/toggle a task with an ID that doesn't exist?
- How does the system handle titles that are exactly 100 characters long vs. those that exceed this limit?
- What happens when all tasks are deleted and the user tries to view the list?
- How does the system handle special characters in titles and descriptions?
- What happens when creating the first task (ID should be 1) and subsequent tasks (IDs should increment)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a console-based menu interface with options 1-6 for task management operations
- **FR-002**: System MUST allow users to create tasks with mandatory title (1-100 characters, printable Unicode including special characters and emojis) and optional description (up to 500 characters, printable Unicode including special characters and emojis)
- **FR-003**: System MUST assign unique numeric IDs to tasks using auto-increment (max(existing_ids)+1) that are permanent and never reused even after task deletion
- **FR-004**: System MUST store tasks in-memory only with no persistent storage to disk
- **FR-005**: System MUST display all tasks in a rich table format with columns: ID, Title, Description, Status, Created At (ISO 8601 format), Last Updated (ISO 8601 format)
- **FR-006**: System MUST show green checkmark indicators for completed tasks
- **FR-007**: System MUST allow users to edit existing tasks by ID, updating title and/or description
- **FR-008**: System MUST allow users to delete tasks by ID
- **FR-009**: System MUST allow users to toggle task status between PENDING and COMPLETED by ID
- **FR-010**: System MUST validate that task IDs exist before allowing edit/delete/toggle operations
- **FR-011**: System MUST update the 'Last Updated' timestamp whenever a task is modified
- **FR-012**: System MUST sort tasks in ascending order by ID when displaying the list
- **FR-013**: System MUST display "No tasks available" when the task list is empty
- **FR-014**: System MUST provide specific error messages that clearly indicate what went wrong and how to fix it for invalid operations
- **FR-018**: System MUST handle errors gracefully with user-friendly messages while allowing the application to continue running
- **FR-015**: System MUST follow clean architecture principles with repository, service, and UI layers
- **FR-016**: System MUST use strict type hints throughout the codebase
- **FR-017**: System MUST implement repository pattern for data access operations

### Key Entities

- **Task**: Represents a single to-do item with properties: ID (unique integer), Title (string, 1-100 chars, printable Unicode including special characters and emojis), Description (optional string, up to 500 chars, printable Unicode including special characters and emojis), Status (PENDING/COMPLETED enum), Created At (timestamp in ISO 8601 format), Last Updated (timestamp in ISO 8601 format)
- **TaskRepository**: Manages in-memory storage of tasks with CRUD operations for single-user access
- **TaskService**: Implements business logic for task operations
- **TaskUI**: Handles user interface and console interactions for single-user console application

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create, view, edit, delete, and toggle tasks through the console interface without data loss during the session
- **SC-002**: All user operations complete in under 2 seconds for datasets up to 1000 tasks
- **SC-003**: 100% of CRUD and toggle operations function correctly as verified by unit tests
- **SC-004**: The system passes mypy --strict validation with zero errors
- **SC-005**: All user-facing messages are clear and helpful, with appropriate error handling for invalid inputs
- **SC-006**: The application follows clean architecture principles with proper separation of concerns between repository, service, and UI layers
