from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

# Base schema for common fields
class UserBase(BaseModel):
    user_id: str  # Using user_id as the phone number
    name: str
    # email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a new user
class UserCreate(UserBase):
    address: str
    # phone: str
    # password: str  # Include password during creation

# Schema for updating an existing user
class UserUpdate(BaseModel):
    name: Optional[str]
    # email: Optional[EmailStr]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Response schema for User
class User(UserBase):
    user_id: str  # Unique identifier for the user

    class Config:
        orm_mode = True
