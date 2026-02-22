from sqlalchemy.orm import Session
from .model import User
from .schema import UserCreate, UserUpdate
from uuid import UUID


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_in: UserCreate, hashed_password: str = None) -> User:
        user_data = user_in.model_dump(exclude={"password"})
        db_user = User(**user_data, hashed_password=hashed_password)

        self.db.add(db_user)
        self.db.flush()
        return db_user

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def delete(self, db_user: User) -> None:
        self.db.delete(db_user)
        return True
