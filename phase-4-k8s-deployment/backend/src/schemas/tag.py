"""Tag Schemas

Pydantic schemas for tag request/response validation and serialization.
"""

from pydantic import BaseModel, Field


class TagWithUsage(BaseModel):
    """Schema for tag autocomplete responses showing tag usage statistics.

    Attributes:
        name: Tag name
        usage_count: Number of tasks using this tag
    """

    name: str = Field(description="Tag name")
    usage_count: int = Field(description="Number of tasks using this tag")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "urgent",
                    "usage_count": 5
                }
            ]
        }
    }
