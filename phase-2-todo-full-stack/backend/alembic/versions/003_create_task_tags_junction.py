"""Create task_tags junction table

Revision ID: 003_create_task_tags
Revises: 002_create_tags
Create Date: 2025-12-30

Creates many-to-many junction table linking tasks to tags.
Includes CASCADE delete behavior - when a task or tag is deleted,
the associations are automatically removed.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003_create_task_tags'
down_revision: Union[str, None] = '002_create_tags'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create task_tags junction table for many-to-many relationship.

    Columns:
    - task_id: UUID, foreign key to tasks.id (CASCADE delete)
    - tag_id: UUID, foreign key to tags.id (CASCADE delete)

    Constraints:
    - Composite primary key on (task_id, tag_id)
    - Foreign keys with CASCADE delete

    Indexes:
    - Index on tag_id for reverse lookups (all tasks with a specific tag)
    """
    op.create_table(
        'task_tags',
        sa.Column('task_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ['task_id'],
            ['tasks.id'],
            name='fk_task_tags_task_id',
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['tag_id'],
            ['tags.id'],
            name='fk_task_tags_tag_id',
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('task_id', 'tag_id')
    )

    # Create index for reverse lookups (all tasks with a specific tag)
    op.create_index('ix_task_tags_tag_id', 'task_tags', ['tag_id'], unique=False)


def downgrade() -> None:
    """
    Drop task_tags junction table and indexes.
    """
    op.drop_index('ix_task_tags_tag_id', table_name='task_tags')
    op.drop_table('task_tags')
