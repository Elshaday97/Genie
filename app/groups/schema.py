from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from uuid import UUID
from typing import Optional


class FamilyGroupBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=100)


class FamilyGroupCreate(FamilyGroupBase):
    group_image: Optional[HttpUrl] = None


class FamilyGroupUpdate(FamilyGroupBase):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=255)
    group_image: Optional[HttpUrl] = None


class GroupMembersUpdate(BaseModel):
    user_id: UUID


class FamilyGroupRead(BaseModel):
    id: UUID
    name: str
    description: str
    owner_id: UUID

    member_count: int

    model_config = ConfigDict(from_attributes=True)
