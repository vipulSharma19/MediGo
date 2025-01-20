from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields (inherited from Entity)
class OrderConfirmationBase(BaseModel):
    confirmation_status: str
    confirmation_timestamp: datetime
    created_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a new order confirmation
class OrderConfirmationCreate(OrderConfirmationBase):
    order_id: UUID

# Schema for updating an existing order confirmation
class OrderConfirmationUpdate(BaseModel):
    confirmation_status: Optional[str]
    confirmation_timestamp: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

# Response schema for Order Confirmation
class OrderConfirmation(OrderConfirmationCreate):
    confirmation_id: UUID  # Unique confirmation ID
    order_id: UUID  # Reference to the parent Order

    class Config:
        orm_mode = True
