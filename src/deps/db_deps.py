from src.db.database import async_session
from fastapi import Request


async def get_db():
    async with async_session() as session:
        yield session

