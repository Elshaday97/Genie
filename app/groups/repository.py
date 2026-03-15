from sqlalchemy.orm import Session
from .schema import FamilyGroupCreate, FamilyGroupRead, FamilyGroupUpdate
from uuid import UUID
from .model import FamilyGroup, FamilyGroupMember
from typing import List
from app.users.model import User


class FamilyGroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, group_in: FamilyGroupCreate, owner_id: UUID):
        db_group = FamilyGroup(**group_in.model_dump(), owner_id=owner_id)

        self.db.add(db_group)
        self.db.flush()

        member_link = FamilyGroupMember(group_id=db_group.id, user_id=owner_id)
        self.db.add(member_link)
        self.db.flush()

        return db_group

    def get_by_id(self, group_id: UUID) -> FamilyGroup:
        return self.db.query(FamilyGroup).filter(FamilyGroup.id == group_id).first()

    def get_by_user_id(
        self, current_user_id: UUID, skip: int, limit: int
    ) -> List[FamilyGroup]:
        return (
            self.db.query(FamilyGroup)
            .filter(FamilyGroup.owner_id == current_user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_members(self, group_id: UUID, skip: int, limit: int) -> List[FamilyGroup]:
        return (
            self.db.query(User)
            .join(FamilyGroupMember, User.id == FamilyGroupMember.user_id)
            .filter(FamilyGroupMember.group_id == group_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete(self, group: FamilyGroup):
        self.db.delete(group)
