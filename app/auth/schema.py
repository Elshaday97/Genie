from fastapi import Form
from pydantic import BaseModel, Field
from .enums import TokenTypesEnum
from typing import Optional
from app.utils.validators import PhoneNumber


class Auth(BaseModel):
    access_token: str
    refresh_token: str
    token_type: TokenTypesEnum = TokenTypesEnum.BEARER


class OAuth2RefreshRequestForm:
    def __init__(
        self,
        grant_type: str = Form(None, pattern="^refresh_token$"),
        refresh_token: str = Form(...),
    ):
        self.grant_type = grant_type
        self.refresh_token = refresh_token


class OTPRequest(BaseModel):
    phone_number: PhoneNumber


class OTPVerify(BaseModel):
    code: str = Field(min_length=6, max_length=6)
    phone_number: PhoneNumber
