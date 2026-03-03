from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.db_deps import get_db
from src.deps.auth_deps import get_current_user
from src.services.auth_service import AuthService
from src.schemas.auth_schema import UserCreate, UserLogin, TokenResponse, LogoutRequest
from src.core.exceptions import BaseAppException
from src.core.config import settings
from src.utils.logger import logger

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", summary="Регистрация нового пользователя")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService()
    try:
        await service.register(db, user_data)
        return {"msg": "Пользователь успешно зарегистрирован"}
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@auth_router.post("/login", response_model=TokenResponse, summary="Вход в систему")
async def login(
    request: Request,
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService()
    try:
        tokens = await service.login(db, user_data, request)
        response = Response()
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        return tokens
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@auth_router.post("/refresh", response_model=TokenResponse, summary="Обновление токенов")
async def refresh(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        body = await request.json()
        refresh_token = body.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    service = AuthService()
    try:
        tokens = await service.refresh_tokens(refresh_token, request)
        response = Response()
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        return tokens
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@auth_router.post("/logout")
async def logout(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing access token")
    access_token = auth_header.split(" ")[1]

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        body = await request.json()
        refresh_token = body.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    service = AuthService()
    try:
        await service.logout(access_token, current_user.id, refresh_token, request)
        response = Response()
        response.delete_cookie("refresh_token")
        return {"msg": "Успешный выход"}
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@auth_router.post("/logout-all")
async def logout_all(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = AuthService()
    try:
        await service.logout_all(current_user.id)
        response = Response()
        response.delete_cookie("refresh_token")
        return {"msg": "Вы вышли со всех устройств"}
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)