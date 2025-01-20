from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields
class StoreBase(BaseModel):
    tenant_id: UUID
    name: str  # Store name
    address: str
    contact_email: EmailStr
    phone: str
    proprietor_name: Optional[str] = None  # Proprietor's name
    dl_no: Optional[str] = None  # DL number
    dl_license_photo: Optional[str] = None  # Base64-encoded DL license photo
    gst_pan_number: Optional[str] = None  # GST/PAN number
    gst_certificate_img: Optional[str] = None  # Base64-encoded GST certificate
    govt_id: Optional[str] = None  # Government ID (e.g., Aadhar)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a new store
class StoreCreate(StoreBase):
    pass  # Use all fields from StoreBase for creation

# Schema for updating an existing store
class StoreUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    contact_email: Optional[EmailStr]
    phone: Optional[str]
    proprietor_name: Optional[str] = None
    dl_no: Optional[str] = None
    dl_license_photo: Optional[str] = None
    gst_pan_number: Optional[str] = None
    gst_certificate_img: Optional[str] = None
    govt_id: Optional[str] = None
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Response schema for Store
class Store(StoreBase):
    store_id: UUID  # Unique identifier for the store

    class Config:
        orm_mode = True
