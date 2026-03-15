from fastapi import APIRouter, Depends, status
from .constants import FAMILY_GROUP_PREFIX, FAMILY_GROUP_TAG
from .service import FamilyGroupService
from sqlalchemy.orm import Session
from app.api.deps import get_db, PaginationParams
from app.auth.deps import get_active_user
from typing import List
from .schema import (
    FamilyGroupCreate,
    FamilyGroupUpdate,
    FamilyGroupRead,
    GroupMembersUpdate,
)
from uuid import UUID
from app.users.model import User
from app.users.schema import UserRead

router = APIRouter(prefix=FAMILY_GROUP_PREFIX, tags=FAMILY_GROUP_TAG)


def get_family_group_service(db: Session = Depends(get_db)) -> FamilyGroupService:
    return FamilyGroupService(db)


@router.post(
    "/",
    response_model=FamilyGroupRead,
    status_code=status.HTTP_201_CREATED,
    description="Create a Family Group",
)
def create_family_group(
    data: FamilyGroupCreate,
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.create_family_group(group_in=data, owner_id=current_user.id)


@router.get(
    "/{group_id}", response_model=FamilyGroupRead, description="Get Family Group by ID"
)
def get_family_group_by_id(
    group_id: UUID,
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.get_family_group_by_id(
        group_id=group_id, current_user_id=current_user.id
    )


@router.put(
    "/{group_id}", response_model=FamilyGroupRead, description="Update Family Group"
)
def update_family_group(
    group_id: UUID,
    data: FamilyGroupUpdate,
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.update_family_group(
        group_id=group_id, group_in=data, current_user_id=current_user.id
    )


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a Family Group",
)
def delete_family_group(
    group_id: UUID,
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.delete_family_group(
        group_id=group_id, current_user_id=current_user.id
    )


@router.get(
    "/", response_model=List[FamilyGroupRead], description="Get user's family groups"
)
def get_user_family_groups(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.get_user_family_groups(
        current_user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit,
    )


@router.post(
    "/{group_id}/members",
    description="Add members to family group",
)
def add_members_to_group(
    group_id: UUID,
    members: List[GroupMembersUpdate],
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.add_members_to_group(
        group_id=group_id, members_in=members, current_user_id=current_user.id
    )


@router.get(
    "/{group_id}/members",
    response_model=List[UserRead],
    description="Get Family Group Members",
)
def get_group_members(
    group_id: UUID,
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.get_group_members(
        group_id=group_id,
        current_user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit,
    )


@router.delete(
    "/{group_id}/member/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a member from a Family Group",
)
def remove_member_from_group(
    group_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_active_user),
    service: FamilyGroupService = Depends(get_family_group_service),
):
    return service.remove_member_from_group(
        group_id=group_id, user_id=user_id, current_user_id=current_user.id
    )
