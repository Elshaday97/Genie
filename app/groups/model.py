from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import String, DateTime, ForeignKey, Enum, select, func
from typing import Optional, List
from sqlalchemy.sql import func
from uuid import UUID, uuid4
from .enums import FamilyGroupStatusEnum


class FamilyGroupMember(Base):
    __tablename__ = "family_group_members"

    group_id: Mapped[UUID] = mapped_column(
        ForeignKey("family_groups.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )

    # Timestamps
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class FamilyGroup(Base):
    __tablename__ = "family_groups"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, unique=True, default=uuid4, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(50))

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[FamilyGroupStatusEnum] = mapped_column(
        Enum(
            FamilyGroupStatusEnum,
            name="familygroupstatusenum",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        default=FamilyGroupStatusEnum.ACTIVE.value,
        server_default=FamilyGroupStatusEnum.ACTIVE.value,
    )

    group_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    members: Mapped[List["User"]] = relationship(
        "User", secondary="family_group_members", back_populates="family_groups"
    )

    member_count: Mapped[int] = column_property(
        select(func.count(FamilyGroupMember.user_id))
        .where(FamilyGroupMember.group_id == id)
        .correlate_except(FamilyGroupMember)
        .scalar_subquery()
    )

    # Relations
    owner: Mapped["User"] = relationship("User", back_populates="owned_groups")

    # Timestamps
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
