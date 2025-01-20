from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields (inherited from Entity)
class OrderBase(BaseModel):
    medicine_names: str
    store_id: UUID
    status: str
    total_amount: float
    payment_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a new order
class OrderCreate(OrderBase):
    entity_id: UUID

# Schema for updating an existing order
class OrderUpdate(BaseModel):
    medicine_names: Optional[str]
    store_id: Optional[UUID]
    status: Optional[str]
    total_amount: Optional[float]
    payment_status: Optional[str]

    class Config:
        orm_mode = True

# Response schema for Order (including order_id)
class Order(OrderCreate):
    order_id: UUID  # Unique order ID, inheriting from EntityBase
    entity_id: UUID  # Reference to the parent Entity

    class Config:
        orm_mode = True
