from sqlalchemy.orm import Session
from .repository import UserRepository
from .model import User
from .schema import UserCreate, UserUpdate
from fastapi import HTTPException, status
from uuid import UUID
from app.utils.security import hash_password
from sqlalchemy.exc import IntegrityError
from app.exceptions.mappers import parse_integrity_error


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> User:
        hashed_password = hash_password(user_in.password) if user_in.password else None

        try:
            user = self.repository.create(user_in, hashed_password)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=parse_integrity_error(e)
            )
        except Exception:
            self.db.rollback()
            raise

    def get_user_by_id(self, user_id: UUID) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists"
            )
        return user

    def update_user(self, user_id: UUID, user_in: UserUpdate) -> User:
        db_user = self.get_user_by_id(user_id)
        update_data = user_in.model_dump(exclude_unset=True)

        try:
            for field, value in update_data.items():
                setattr(db_user, field, value)

            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=parse_integrity_error(e)
            )

    def delete_user(self, user_id: UUID):
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        try:
            self.repository.delete(db_user)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User could not be deleted.",
            )
