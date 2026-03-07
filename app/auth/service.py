from sqlalchemy.orm import Session
from app.users.repository import UserRepository
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.utils.security import (
    verify_password,
    decode_token,
    create_access_token,
    create_refresh_token,
)
from .schema import Auth
from app.users.model import User
from .model import OTPTracking
from app.utils.otp import send_otp, check_otp
from datetime import datetime, timezone
from app.core.config import config
from .enums import AuthResponseEnums
from app.users.enums import UserStatusEnum


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def authenticate_user(self, username: str, plain_password: str) -> Auth:
        invalid_credentials_exp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = self.user_repository.get_by_username(username)
        if not user or not verify_password(
            plain_password, hashed_password=user.hashed_password
        ):
            raise invalid_credentials_exp

        token_payload = {"sub": str(user.id)}
        return Auth(
            access_token=create_access_token(token_payload),
            refresh_token=create_refresh_token(token_payload),
        )

    def refresh_token(self, refresh_token: str) -> Auth:

        payload = decode_token(refresh_token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not exist",
            )
        token_payload = {"sub": str(user.id)}

        return Auth(
            access_token=create_access_token(token_payload),
            refresh_token=create_refresh_token(token_payload),
        )

    def request_otp(self, phone_number):
        user = self.db.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phone number does not exist",
            )

        now = datetime.now(timezone.utc)
        otp_tracking = (
            self.db.query(OTPTracking)
            .filter(OTPTracking.phone_number == phone_number)
            .first()
        )

        if otp_tracking:
            difference = now - otp_tracking.last_sent

            if difference.total_seconds() < config.OTP_VALIDITY_SECONDS:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Can not send OTP. Too many requests.",
                )

            otp_tracking.last_sent = now
            otp_tracking.send_count += 1

        else:
            otp_tracking = OTPTracking(
                last_sent=now,
                user_id=user.id,
                phone_number=user.phone_number,
                is_verified=False,
                send_count=1,
            )
            self.db.add(otp_tracking)

        send_otp(phone_number=phone_number)
        self.db.commit()

        return {"message": AuthResponseEnums.OTP_SENT}

    def verify_otp(self, phone_number: str, code: str):
        user = self.db.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phone number does not exist",
            )

        otp_tracking = (
            self.db.query(OTPTracking)
            .filter(OTPTracking.phone_number == phone_number)
            .first()
        )

        if not otp_tracking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No OTP requested to this phone number",
            )

        check_otp(phone_number, code)

        user.status = UserStatusEnum.ACTIVE
        user.is_active = True
        user.is_verified = True

        self.db.delete(otp_tracking)

        self.db.commit()

        token_payload = {"sub": str(user.id)}

        return Auth(
            access_token=create_access_token(token_payload),
            refresh_token=create_refresh_token(token_payload),
        )
