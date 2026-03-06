from enum import Enum

class RoleName(str, Enum):
    APPLICANT = "applicant"
    COMPANY = "company"

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    VIEWED = "viewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"