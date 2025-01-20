from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields
class EntityBase(BaseModel):
    entity_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Ensures compatibility with SQLAlchemy models

# Schema for creating a new entity
class EntityCreate(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for updating an existing entity
class EntityUpdate(BaseModel):
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Response schema for Entity
class Entity(EntityBase):
    pass  # Inherits all fields from EntityBase
