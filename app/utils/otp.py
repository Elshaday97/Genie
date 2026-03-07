from twilio.rest import Client
from app.core.config import config
from fastapi import status, HTTPException
from app.auth.enums import TwilioStatusEnum, AuthResponseEnums

client = Client(
    account_sid=config.TWILIO_ACCOUNT_SID,
)


def send_otp(phone_number: str):
    try:
        verification = client.verify.v2.services(
            config.TWILIO_VERIFY_SERVICE_SID
        ).verifications.create(to=phone_number, channel="sms")

        return
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to send OTP. {e}"
        )


def check_otp(phone_number: str, code: str):
    try:
        verification_check = client.verify.v2.services(
            config.TWILIO_VERIFY_SERVICE_SID
        ).verification_checks.create(to=phone_number, code=code)

    except Exception as e:
        print(f"{AuthResponseEnums.OTP_VERIFY_FAILED}:{e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error communicating with SMS provider.",
        )

    if verification_check.status == TwilioStatusEnum.APPROVED.value:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to verify OTP",
        )
