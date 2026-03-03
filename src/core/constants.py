from enum import Enum

class RoleName(str, Enum):
    APPLICANT = "applicant"
    COMPANY = "company"

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"