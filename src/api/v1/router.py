from fastapi import APIRouter

from src.api.v1.auth_router import auth_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)