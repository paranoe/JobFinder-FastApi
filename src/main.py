from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.v1.router import api_router
from src.redis.client import redis_client
from src.redis.auth import session_manager
from src.core.exceptions import app_exception_handler, BaseAppException
from src.utils.logger import logger
from src.models.seed import seed_all

@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_all()
    await redis_client.connect()
    await session_manager.initialize() 
    logger.info("Application started")
    yield
    await redis_client.close()
    logger.info("Application stopped")

app = FastAPI(lifespan=lifespan, title="Auth Service")


app.add_exception_handler(BaseAppException, app_exception_handler)


app.include_router(api_router)