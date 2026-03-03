from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    LOGIN_RATE_LIMIT: int = 5        
    LOGIN_RATE_WINDOW: int = 300        
    REFRESH_RATE_LIMIT: int = 10
    REFRESH_RATE_WINDOW: int = 300
    
    MAX_SESSIONS_PER_USER: int = 5
    ENVIRONMENT: str = "development"


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )



settings = Settings()