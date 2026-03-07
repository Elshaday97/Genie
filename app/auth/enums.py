import enum


class TokenTypesEnum(str, enum.Enum):
    BEARER = "bearer"


class AuthResponseEnums(str, enum.Enum):
    OTP_SENT = "OTP_SENT"
    OTP_VERIFIED = "OTP_VERIFIED"
    OTP_VERIFY_FAILED = "OTP_VERIFY_FAILED"


class TwilioStatusEnum(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    CANCELED = "canceled"
    MAX_ATTEMPTS_REACHED = "max_attempts_reached"
    DELETED = "deleted"
    FAILED = "failed"
    EXPIRED = "expired"
