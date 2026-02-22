from enum import Enum


class UserStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class UserTierEnum(str, Enum):
    FREE = "free"
    SILVER = "silver"
    GOLD = "gold"
    DIAMOND = "diamond"
