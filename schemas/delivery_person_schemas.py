from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields (inherited from Entity)
class DeliveryPersonBase(BaseModel):
    name: str
    phone: str
    vehicle_type: str
    vehicle_number: Optional[str] = None  # Vehicle number is optional
    vehicle_img: Optional[str] = None  # Base64-encoded vehicle image
    license_photo: Optional[str] = None  # Base64-encoded license photo
    rc: Optional[str] = None  # Base64-encoded RC
    aadhar_govt_id: Optional[str] = None  # Base64-encoded Aadhar/Govt ID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a new delivery person profile
class DeliveryPersonCreate(DeliveryPersonBase):
    pass

# Schema for updating an existing delivery person profile (partial fields)
class DeliveryPersonUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    vehicle_type: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Response schema for DeliveryPerson
class DeliveryPerson(DeliveryPersonCreate):
    delivery_person_id: UUID  # Unique delivery person ID
    entity_id: UUID  # Reference to the parent Entity

    class Config:
        orm_mode = True
