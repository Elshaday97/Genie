from fastapi import APIRouter, Depends, status
from .constants import AUTH_ROUTE_PREFIX, AUTH_ROUTE_TAG
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from .service import AuthService
from .schema import Auth, OAuth2RefreshRequestForm
from app.api.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix=AUTH_ROUTE_PREFIX, tags=AUTH_ROUTE_TAG)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/login", response_model=Auth, status_code=status.HTTP_200_OK)
def log_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthService = Depends(get_auth_service),
):
    return service.authenticate_user(
        username=form_data.username, plain_password=form_data.password
    )


@router.post("/refresh", response_model=Auth, status_code=status.HTTP_200_OK)
def refresh_token(
    form_data: Annotated[OAuth2RefreshRequestForm, Depends()],
    service: AuthService = Depends(get_auth_service),
):
    return service.refresh_token(form_data.refresh_token)
