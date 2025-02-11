from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class StoreBase(BaseModel):
    store_id: UUID
    name: str
    address: str
    email: Optional[EmailStr]
    phone: str
    proprietor_name: Optional[str] = None
    dl_no: Optional[str] = None
    dl_license_photo: Optional[str] = None
    gst_pan_number: Optional[str] = None
    gst_certificate_img: Optional[str] = None
    govt_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        orm_mode = True

class StoreCreate(StoreBase):
    latitude: float
    longitude: float

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
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        orm_mode = True

class Store(StoreBase):
    store_id: UUID

    class Config:
        orm_mode = True
