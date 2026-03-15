from enum import Enum


class GroupRoleEnum(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class FamilyGroupStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
