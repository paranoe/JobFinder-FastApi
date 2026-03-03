from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

class InvalidTokenError(BaseAppException):
    def __init__(self, message: str = "Невалидный токен"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class ExpiredTokenError(BaseAppException):
    def __init__(self, message: str = "Срок действия токена истёк"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class TokenRevokedError(BaseAppException):
    def __init__(self, message: str = "Токен отозван"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class MissingClaimError(BaseAppException):
    def __init__(self, message: str = "Отсутствуют необходимые claims"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class InvalidCredentialsError(BaseAppException):
    def __init__(self, message: str = "Неверный email или пароль"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class UserInactiveError(BaseAppException):
    def __init__(self, message: str = "Пользователь деактивирован"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)

class RateLimitExceededError(BaseAppException):
    def __init__(self, message: str = "Слишком много запросов"):
        super().__init__(message, status_code=status.HTTP_429_TOO_MANY_REQUESTS)

async def app_exception_handler(request: Request, exc: BaseAppException):
    logger.error(f"App exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )