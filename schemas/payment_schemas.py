from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields (inherited from Entity)
class PaymentBase(BaseModel):
    order_id: UUID
    user_id: str  # New field to include user_id
    amount: float
    payment_method: str
    payment_status: str
    payment_timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a new payment record
class PaymentCreate(PaymentBase):
    pass

# Schema for updating an existing payment record (partial fields)
class PaymentUpdate(BaseModel):
    order_id: Optional[UUID]
    user_id: Optional[str]  # Allow optional update for user_id
    amount: Optional[float]
    payment_method: Optional[str]
    payment_status: Optional[str]
    payment_timestamp: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Response schema for Payment
class Payment(PaymentCreate):
    payment_id: UUID  # Unique payment ID
    order_id: UUID  # Reference to the parent Order
    user_id: str  # Reference to the user making the payment

    class Config:
        orm_mode = True
