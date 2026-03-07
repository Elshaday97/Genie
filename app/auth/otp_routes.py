from fastapi import APIRouter, Depends
from .constants import OTP_ROUTE_PREFIX, OTP_ROUTE_TAG
from .schema import OTPRequest, OTPVerify
from .service import AuthService
from sqlalchemy.orm import Session
from app.api.deps import get_db
from .schema import Auth


router = APIRouter(prefix=OTP_ROUTE_PREFIX, tags=OTP_ROUTE_TAG)


def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)


@router.post("/request")
def request_otp(
    form_data: OTPRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.request_otp(form_data.phone_number)


@router.post("/verify", response_model=Auth)
def verify_otp(form_data: OTPVerify, service: AuthService = Depends(get_auth_service)):
    return service.verify_otp(phone_number=form_data.phone_number, code=form_data.code)
