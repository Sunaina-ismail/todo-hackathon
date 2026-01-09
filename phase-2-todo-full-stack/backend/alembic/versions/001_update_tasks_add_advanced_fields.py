"""Update tasks table with advanced fields (UUID, priority, due_date)

Revision ID: 001_update_tasks
Revises: 4f6b03aa2f5c
Create Date: 2025-12-30

CRITICAL WARNING: This migration changes id from INTEGER to UUID.
This is a destructive operation that will:
1. Drop existing data
2. Recreate the table with UUID primary key
3. Add priority and due_date fields

BACKUP YOUR DATA BEFORE RUNNING THIS MIGRATION!
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_update_tasks'
down_revision: Union[str, None] = '4f6b03aa2f5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade tasks table to support advanced features.

    Changes:
    - Change id from INTEGER to UUID
    - Add priority column (VARCHAR, default 'Medium')
    - Add due_date column (DATE, nullable)
    - Add composite index on (user_id, completed)

    WARNING: This drops and recreates the table!
    """
    # Drop existing table (WARNING: This deletes all data!)
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')

    # Recreate table with UUID and new fields
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('priority', sa.String(length=10), nullable=False, server_default='Medium'),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for performance
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'], unique=False)
    op.create_index('ix_tasks_user_id_completed', 'tasks', ['user_id', 'completed'], unique=False)


def downgrade() -> None:
    """
    Downgrade tasks table back to INTEGER id without advanced fields.

    WARNING: This drops and recreates the table, deleting all data!
    """
    # Drop new table
    op.drop_index('ix_tasks_user_id_completed', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')

    # Recreate original table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'], unique=False)
