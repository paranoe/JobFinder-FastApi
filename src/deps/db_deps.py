from src.db.database import async_session
from src.redis.redis_client import RedisClient
from fastapi import Request


async def get_db():
    async with async_session() as session:
        yield session

def get_redis_service(request: Request) -> RedisClient:
    return request.app.state.redis_client