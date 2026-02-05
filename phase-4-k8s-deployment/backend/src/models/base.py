"""SQLModel Base Configuration

Base class and common utilities for all database models.
"""

from sqlmodel import SQLModel

# SQLModel is both the base class and ORM
# All models inherit from SQLModel with table=True

__all__ = ["SQLModel"]
