"""Create tags table

Revision ID: 002_create_tags
Revises: 001_update_tasks
Create Date: 2025-12-30

Creates tags table for user-defined task categorization.
Tags are user-scoped with unique constraint on (user_id, name).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002_create_tags'
down_revision: Union[str, None] = '001_update_tasks'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create tags table with user isolation and unique constraint.

    Columns:
    - id: UUID primary key
    - name: String(50), tag name
    - user_id: String, Better Auth user ID
    - created_at: DateTime

    Indexes:
    - Composite unique index on (user_id, name)
    - Index on user_id for efficient filtering
    """
    op.create_table(
        'tags',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_tags_user_id', 'tags', ['user_id'], unique=False)
    op.create_index('ix_tags_user_id_name', 'tags', ['user_id', 'name'], unique=True)


def downgrade() -> None:
    """
    Drop tags table and indexes.
    """
    op.drop_index('ix_tags_user_id_name', table_name='tags')
    op.drop_index('ix_tags_user_id', table_name='tags')
    op.drop_table('tags')
