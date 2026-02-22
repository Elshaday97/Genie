import phonenumbers
from typing import Annotated
from pydantic import AfterValidator


def validate_phone(cls, v: str) -> str:
    if v is None:
        return v

    try:
        pn = phonenumbers.parse(v, None)

        if not phonenumbers.is_valid_number(pn):
            raise ValueError("Invalid Phone Number Format")

        return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        raise ValueError("Phone number must include country code")


PhoneNumber = Annotated[str, AfterValidator(validate_phone)]
