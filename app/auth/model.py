from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, ForeignKey, Integer, Boolean
from sqlalchemy.sql import func
import uuid


class OTPTracking(Base):
    __tablename__ = "otp_trackings"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    phone_number: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    send_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Timestamp
    last_sent: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
