import phonenumbers
from typing import Annotated
from pydantic import AfterValidator


import phonenumbers
from typing import Annotated
from pydantic import AfterValidator


def validate_phone(v: str) -> str:
    try:
        pn = phonenumbers.parse(v, None)

        if not phonenumbers.is_valid_number(pn):
            raise ValueError("Invalid phone number format")

        return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)

    except phonenumbers.NumberParseException as e:
        raise ValueError(f"Invalid phone number format: {e}")


PhoneNumber = Annotated[str, AfterValidator(validate_phone)]
