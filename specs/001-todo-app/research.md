# Research Notes: Todo In-Memory Python Console App

## Decision: Task Status Implementation
**Rationale**: Using an Enum for task status (PENDING/COMPLETED) as specified in the feature requirements. This provides type safety and prevents invalid status values.
**Alternatives considered**: Boolean flag, string constants - Enum was chosen for better type safety and extensibility.

## Decision: Rich Table Display
**Rationale**: Using the `rich` library for displaying tasks in a formatted table as specified in the requirements. This provides professional-looking console output with color support.
**Alternatives considered**: Basic print formatting, tabulate library - Rich was chosen for its superior formatting capabilities and ANSI color support.

## Decision: In-Memory Storage Implementation
**Rationale**: Using a Python list within a repository class to store tasks in memory, as required by the specification (no persistent storage). The repository pattern provides clean separation of data access logic.
**Alternatives considered**: Dictionary with ID keys, other data structures - List was chosen for simplicity and natural fit with the auto-incrementing ID requirement.

## Decision: ID Generation Strategy
**Rationale**: Implementing auto-incrementing IDs using max(existing_ids)+1 as specified, with permanent IDs that are never reused after deletion. This ensures ID uniqueness and permanence as clarified in the specification.
**Alternatives considered**: Sequential counter, UUIDs - Max+1 approach was chosen as specified in requirements.

## Decision: Timestamp Format
**Rationale**: Using datetime objects internally and formatting to ISO 8601 string (YYYY-MM-DD HH:MM:SS) for display as specified in the clarifications.
**Alternatives considered**: Unix timestamps, custom formats - ISO 8601 was chosen as specified in clarifications.

## Decision: Validation Implementation
**Rationale**: Implementing validation in the model layer with specific error messages as clarified in the specification. Using dataclasses with validation methods to ensure data integrity.
**Alternatives considered**: Validation in service layer, UI layer - Model layer was chosen for early validation and data integrity.

## Decision: Console Menu Structure
**Rationale**: Implementing the 6-option menu as specified in the requirements (Add, View, Edit, Delete, Toggle, Exit) with proper error handling for invalid inputs.
**Alternatives considered**: Different menu structures - The specified structure was chosen to match requirements exactly.