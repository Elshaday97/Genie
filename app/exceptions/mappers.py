from sqlalchemy.exc import IntegrityError
from app.core.constants import (
    UQ_USER_EMAIL,
    UQ_USER_PHONE,
    UQ_USER_USERNAME,
    FK_FAMILY_GROUP_OWNER,
    FK_GROUP_MEMBERS_GROUP,
    FK_GROUP_MEMBERS_USER,
    MAX_DB_RETRIES,
    PK_FAMILY_GROUP_MEMBERS,
)


def parse_integrity_error(e: IntegrityError) -> str:
    """Parses DB constraints into user-friendly messages."""
    try:
        constraint_name = getattr(e.orig.diag, "constraint_name", None)
    except AttributeError:
        return "A data conflict occurred."

    constraint_map = {
        # User Constraints
        UQ_USER_EMAIL: "Email already exists.",
        UQ_USER_PHONE: "Phone number already exists.",
        UQ_USER_USERNAME: "Username already exists.",
        # Family Group Constraints
        PK_FAMILY_GROUP_MEMBERS: "This user is already a member of the group.",
        FK_GROUP_MEMBERS_USER: "The user you are trying to add does not exist.",
        FK_GROUP_MEMBERS_GROUP: "The specified family group does not exist.",
        FK_FAMILY_GROUP_OWNER: "Action denied. You cannot delete this user because they are the active owner of a family group. Transfer ownership first.",
    }

    return constraint_map.get(constraint_name, "Unique constraint violated.")
