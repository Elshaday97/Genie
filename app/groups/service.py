from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from .schema import FamilyGroupCreate, FamilyGroupUpdate, GroupMembersUpdate
from .model import FamilyGroup
from .repository import FamilyGroupRepository
from .model import FamilyGroup
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException
from app.exceptions.mappers import parse_integrity_error
from app.users.model import User


class FamilyGroupService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = FamilyGroupRepository(db)

    def _get_group(self, group_id: UUID) -> FamilyGroup | None:
        db_group = self.repository.get_by_id(group_id)

        if not db_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Family Group not found"
            )

        return db_group

    def create_family_group(
        self, group_in: FamilyGroupCreate, owner_id: UUID
    ) -> FamilyGroup:
        try:
            group = self.repository.create(group_in, owner_id)
            self.db.commit()
            self.db.refresh(group)
            return group
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=parse_integrity_error(e)
            )

        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}",
            )

    def get_family_group_by_id(
        self, group_id: UUID, current_user_id: UUID
    ) -> FamilyGroup:
        group = self._get_group(group_id)
        return group

    def get_user_family_groups(
        self, current_user_id: UUID, skip: int, limit: int
    ) -> List[FamilyGroup]:
        groups = self.repository.get_by_user_id(current_user_id, skip, limit)

        if not groups:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User has no family groups",
            )

        return groups

    def update_family_group(
        self, group_id: UUID, group_in: FamilyGroupUpdate, current_user_id: UUID
    ) -> FamilyGroup:
        db_group = self._get_group(group_id)
        update_data = group_in.model_dump(exclude_unset=True)

        try:
            for field, value in update_data.items():
                setattr(db_group, field, value)

            self.db.commit()
            self.db.refresh(db_group)

            return db_group

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=parse_integrity_error(e)
            )

    def add_members_to_group(
        self,
        group_id: UUID,
        members_in: List[GroupMembersUpdate],
        current_user_id: UUID,
    ):
        db_group = self._get_group(group_id)

        if db_group.owner_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only owners can add members.",
            )

        added_users = []

        for member_req in members_in:
            user_to_add = (
                self.db.query(User).filter(User.id == member_req.user_id).first()
            )

            if not user_to_add:
                continue

            if user_to_add not in db_group.members:
                db_group.members.append(user_to_add)
                added_users.append(user_to_add)

        try:
            self.db.commit()
            return {"detail": f"Successfully added {len(added_users)} members."}
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Failed to add members")

    def remove_member_from_group(
        self, group_id: UUID, user_id: UUID, current_user_id: UUID
    ):
        db_group = self._get_group(group_id)

        if db_group.owner_id != current_user_id and current_user_id != user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to remove this member"
            )

        user_to_remove = next((u for u in db_group.members if u.id == user_id), None)

        if not user_to_remove:
            raise HTTPException(
                status_code=404, detail="User is not a member of this group"
            )

        db_group.members.remove(user_to_remove)
        self.db.commit()
        return {"detail": "Member removed successfully"}

    def get_group_members(
        self, group_id: UUID, current_user_id: UUID, skip: int, limit: int
    ) -> List[User]:
        self._get_group(group_id)
        return self.repository.get_members(group_id, skip, limit)

    def delete_family_group(self, group_id: UUID, current_user_id: UUID):
        db_group = self._get_group(group_id)

        try:
            self.repository.delete(group=db_group)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Family group could not be deleted",
            )
