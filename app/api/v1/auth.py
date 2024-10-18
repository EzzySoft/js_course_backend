from fastapi import APIRouter, Depends
from fastapi import Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from models import database_helper
from schemas.user_scheme import CreateUserScheme, CredentialsScheme
from services import auth_service
from services.response_service import ResponseService

router = APIRouter(tags=["Auth"])


@router.post("/signup")
async def sign_up(user: CreateUserScheme, db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        auth_service.register_user(user, db)
    )


@router.post("/login")
async def login(user: CredentialsScheme, db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        auth_service.login_user(user, db)
    )


@router.get("/getusers/me/")
async def get_info(session_id: str | None = Cookie(default=None),
                   db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        auth_service.get_info(session_id, db)
    )


@router.get("/getusers/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(database_helper.session_getter)):
    return await ResponseService.response(
        auth_service.get_user(user_id, db)
    )


@router.post("/logout")
async def logout(session_id: str | None = Cookie(default=None)):
    return await ResponseService.response(
        auth_service.logout(session_id)
    )





