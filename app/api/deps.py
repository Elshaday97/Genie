from typing import Generator
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Query


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # return connection to pool once session is complete


class PaginationParams:
    def __init__(
        self,
        skip: int = Query(
            0, ge=0, description="Number of records to skip for pagination"
        ),
        limit: int = Query(
            10,
            ge=1,
            le=100,
            description="Maximum number of records to return (Max 100)",
        ),
    ):
        self.skip = skip
        self.limit = limit
