from pydantic import Field, BaseModel, EmailStr, HttpUrl, model_validator
from .enums import UserStatusEnum, UserTierEnum
from typing import Optional
from app.utils.validators import PhoneNumber
from uuid import UUID


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=5, max_length=50)
    last_name: str = Field(..., min_length=5, max_length=50)
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = None
    phone_number: PhoneNumber = None
    profile_image: Optional[HttpUrl] = None


class UserCreate(UserBase):
    password: Optional[str] = Field(min_length=8, max_length=50)

    @model_validator(mode="after")
    def check_auth_method(self) -> "UserCreate":
        if not self.password and not self.phone_number:
            raise ValueError(
                "You must provide either a password or a phone number to register."
            )
        return self


class UserUpdate(UserBase):
    first_name: Optional[str] = Field(None, min_length=5, max_length=50)
    last_name: Optional[str] = Field(None, min_length=5, max_length=50)
    username: Optional[str] = Field(None, min_length=5, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: PhoneNumber = None
    tier: Optional[UserTierEnum] = None


class UserRead(UserBase):
    id: UUID
    tier: UserTierEnum
    status: UserStatusEnum
    is_verified: bool

    class Config:
        from_attributes = True
