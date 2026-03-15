from pydantic import Field, BaseModel, EmailStr, HttpUrl, ConfigDict
from .enums import UserStatusEnum, UserTierEnum
from typing import Optional
from app.utils.validators import PhoneNumber
from uuid import UUID


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=5, max_length=50)
    last_name: str = Field(..., min_length=5, max_length=50)
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = None
    phone_number: PhoneNumber
    profile_image: Optional[HttpUrl] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserUpdate(UserBase):
    tier: Optional[UserTierEnum] = None


class UserRead(UserBase):
    id: UUID
    tier: UserTierEnum
    status: UserStatusEnum
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
