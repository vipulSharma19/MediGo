from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields (inherited from Entity)
class DeliveryBase(BaseModel):
    order_id: UUID
    store_id: UUID
    delivery_person_id: UUID
    pickup_location: str
    delivery_location: str
    delivery_fee: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a new delivery task
class DeliveryCreate(DeliveryBase):
    pass

# Schema for updating an existing delivery task (partial fields)
class DeliveryUpdate(BaseModel):
    order_id: Optional[UUID]
    store_id: Optional[UUID]
    delivery_person_id: Optional[UUID]
    pickup_location: Optional[str]
    delivery_location: Optional[str]
    delivery_fee: Optional[float]
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Response schema for Delivery
class Delivery(DeliveryCreate):
    delivery_id: UUID  # Unique delivery ID
    order_id: UUID  # Reference to the parent Order
    store_id: UUID  # Reference to the parent Store
    delivery_person_id: UUID  # Reference to the DeliveryPerson

    class Config:
        orm_mode = True
