# Todo In-Memory Python Console App

A Python console-based task manager with in-memory storage following clean architecture, strict type hints, and repository pattern. The application provides a menu-driven interface for creating, viewing, editing, deleting, and toggling completion status of tasks. The system stores tasks in-memory only with no persistent storage.

## Features

- Create, view, edit, delete, and toggle completion status of tasks
- In-memory storage (no persistent storage)
- Clean architecture with repository, service, and UI layers
- Strict type hints throughout the codebase
- Repository pattern for data access operations
- Support for special characters and emojis in task titles and descriptions
- ISO 8601 timestamp formatting
- Rich table formatting for task display

## Prerequisites

- Python 3.13+
- pip package manager

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python src/cli/main.py
   ```

## Usage

The application provides a menu-driven interface:

1. **Add new task**: Create a new task with a title and optional description
2. **View all tasks**: Display all tasks in a rich table format sorted by ID
3. **Edit task**: Modify the title or description of an existing task
4. **Delete task**: Remove a task by its ID
5. **Toggle task completion**: Switch a task's status between pending and completed
6. **Exit**: Quit the application

## Architecture

The application follows clean architecture principles:

- **Models** (`src/models/`): Contains data models with validation
- **Repositories** (`src/repositories/`): Handles in-memory data storage
- **Services** (`src/services/`): Implements business logic
- **CLI** (`src/cli/`): Handles user interface and console interactions

## Development

1. Run type checking:
   ```bash
   mypy --strict src/
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

## Validation

All user operations complete in under 2 seconds for datasets up to 1000 tasks.
The system passes mypy --strict validation with zero errors.