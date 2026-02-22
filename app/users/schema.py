from pydantic import Field, BaseModel, EmailStr
from .enums import UserStatusEnum, UserTierEnum
from typing import Optional
from app.utils.validators import PhoneNumber
from uuid import UUID


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=5, max_length=50)
    last_name: str = Field(..., min_length=5, max_length=50)
    user_name: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = None
    phone_number: Optional[PhoneNumber] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserUpdate(UserBase):
    first_name: Optional[str] = Field(None, min_length=5, max_length=50)
    last_name: Optional[str] = Field(None, min_length=5, max_length=50)
    user_name: Optional[str] = Field(None, min_length=5, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneNumber] = None
    tier: Optional[UserTierEnum] = None


class UserRead(UserBase):
    id: UUID
    tier: UserTierEnum
    status: UserStatusEnum

    class Config:
        from_attributes = True
