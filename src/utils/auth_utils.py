from src.core.config import setting
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt


class JWTToken:
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({
            "exp": expire,
            "type": "access"
        })
        return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(days=setting.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })
        return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token, 
                setting.SECRET_KEY, 
                algorithms=[setting.ALGORITHM]
            )
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
    @staticmethod
    def verify_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                setting.SECRET_KEY,
                algorithms=[setting.ALGORITHM]
            )
            
            if payload.get("type") != "access":
                return None
                
            return payload
        except JWTError:
            return None
        
    @staticmethod
    def verify_refresh_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                setting.SECRET_KEY,
                algorithms=[setting.ALGORITHM]
            )
            
            if payload.get("type") != "refresh":
                return None
                
            return payload
        except JWTError:
            return None