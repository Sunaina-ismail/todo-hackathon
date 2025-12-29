# Data Model: Todo In-Memory Python Console App

## Task Entity

### Fields
- **id**: `int` - Unique identifier, auto-incremented, permanent (never reused after deletion)
- **title**: `str` - Task title (1-100 characters, printable Unicode including special characters and emojis)
- **description**: `Optional[str]` - Task description (up to 500 characters, printable Unicode including special characters and emojis)
- **status**: `TaskStatus` - Enum value (PENDING or COMPLETED)
- **created_at**: `datetime` - Timestamp when task was created (ISO 8601 format for display)
- **updated_at**: `datetime` - Timestamp when task was last modified (ISO 8601 format for display)

### Validation Rules
- Title must be 1-100 characters (inclusive)
- Description must be 0-500 characters (if provided)
- Title and description must contain printable Unicode characters
- Status must be either PENDING or COMPLETED
- ID must be unique and positive integer

### State Transitions
- **PENDING → COMPLETED**: When user toggles completion status
- **COMPLETED → PENDING**: When user toggles completion status

## TaskStatus Enum
- **PENDING**: Task is not yet completed
- **COMPLETED**: Task has been completed

## TaskRepository Interface
- **create_task(title: str, description: Optional[str])** → Task: Creates a new task with auto-incremented ID
- **get_all_tasks()** → List[Task]: Returns all tasks sorted by ID ascending
- **get_task_by_id(task_id: int)** → Optional[Task]: Returns task with specified ID or None
- **update_task(task_id: int, title: Optional[str], description: Optional[str])** → bool: Updates task details and returns success status
- **delete_task(task_id: int)** → bool: Deletes task and returns success status
- **toggle_task_status(task_id: int)** → bool: Toggles task status and returns success status