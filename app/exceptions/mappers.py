from sqlalchemy.exc import IntegrityError
from app.core.constants import UQ_USER_EMAIL, UQ_USER_PHONE, UQ_USER_USERNAME


def parse_integrity_error(e: IntegrityError) -> str:
    """Parses DB constraints into user-friendly messages."""
    try:
        constraint_name = getattr(e.orig.diag, "constraint_name", None)
    except AttributeError:
        return "A data conflict occurred."

    constraint_map = {
        UQ_USER_EMAIL: "Email already exists.",
        UQ_USER_PHONE: "Phone number already exists.",
        UQ_USER_USERNAME: "Username already exists.",
    }

    return constraint_map.get(constraint_name, "Unique constraint violated.")
