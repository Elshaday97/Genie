from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from .service import UserService
from .schema import UserCreate, UserUpdate, UserRead
from .constants import USER_ROUTE_PREFIX, USER_ROUTE_TAG
from uuid import UUID


router = APIRouter(prefix=USER_ROUTE_PREFIX, tags=USER_ROUTE_TAG)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(data)


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID, data: UserUpdate, service: UserService = Depends(get_user_service)
):
    return service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    service.delete_user(user_id)
    return None
