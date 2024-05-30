from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema for handling tasks model.
    General settings for all schemas."""
    model_config = ConfigDict(from_attributes=True)


class TasksSchema(BaseSchema):
    """Schema for handling tasks model."""
    title: str
    description: str | None = None


class TasksResponseSchema(TasksSchema):
    """Schema for handling tasks response model."""
    id: int
    created_at: datetime
    updated_at: datetime | None


class TaskUpdateSchema(BaseSchema):
    """Schema for handling tasks update model."""
    title: str | None = None
    description: str | None = None
