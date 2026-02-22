import uuid
from typing import List, Optional
from sqlalchemy import String, ForeignKey, DateTime, text, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.session import Base
from app.users.enums import UserStatusEnum, UserTierEnum
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyBaseOAuthAccountTableUUID,
)
from fastapi_users_db_sqlalchemy.generics import GUID
from app.core.constants import UQ_USER_EMAIL, UQ_USER_PHONE, UQ_USER_USERNAME


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__ = "oauth_accounts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="oauth_accounts")


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name=UQ_USER_EMAIL),
        UniqueConstraint("user_name", name=UQ_USER_USERNAME),
        UniqueConstraint("phone_number", name=UQ_USER_PHONE),
    )

    # Personal Information
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    # Auth Fields
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )

    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20), unique=True, index=True
    )

    status: Mapped[UserStatusEnum] = mapped_column(
        Enum(
            UserStatusEnum,
            name="userstatusenum",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        default=UserStatusEnum.PENDING.value,  # Python Default
        server_default=UserStatusEnum.PENDING.value,  # Database Default
    )

    # Subscription & App Logic
    tier: Mapped[UserTierEnum] = mapped_column(
        Enum(
            UserTierEnum,
            name="usertierenum",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        default=UserTierEnum.FREE.value,
        server_default=UserTierEnum.FREE.value,
    )
    family_groups_created: Mapped[int] = mapped_column(
        server_default=text("0"), default=0
    )

    # Relationship
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount",
        lazy="joined",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Timestamps
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
