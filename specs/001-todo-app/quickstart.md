# Quickstart Guide: Todo In-Memory Python Console App

## Prerequisites
- Python 3.13+
- pip package manager

## Setup
1. Install dependencies: `pip install rich`
2. Install type checker: `pip install mypy`

## Running the Application
```bash
cd /path/to/project
python src/cli/main.py
```

## Development
1. Run type checking: `mypy --strict src/`
2. Run tests: `pytest tests/`
3. The application follows clean architecture with repository, service, and UI layers

## Key Components
- **Models**: Located in `src/models/` - Contains data models with validation
- **Repositories**: Located in `src/repositories/` - Handles in-memory data storage
- **Services**: Located in `src/services/` - Implements business logic
- **CLI**: Located in `src/cli/` - Handles user interface and console interactions