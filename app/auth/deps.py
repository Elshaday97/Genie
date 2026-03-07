from app.utils.security import decode_token
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.users.model import User
from fastapi.security import OAuth2PasswordBearer
from app.api.deps import get_db
from app.users.enums import UserStatusEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user


def get_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.status == UserStatusEnum.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active"
        )

    return current_user
