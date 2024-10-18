import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from config import settings
from exceptions import UsernameInUseError, EmailInUseError, UserNotFoundError
from schemas.user_scheme import CreateUserScheme, UserScheme
from models.user_model import User


async def create(user_create: CreateUserScheme, db: AsyncSession) -> UserScheme:
    async def check_username(username: str):
        query = select(User).filter(User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            raise UsernameInUseError

    async def check_email(email: str):
        query = select(User).filter(User.email == email)
        result = await db.execute(query)
        user = result.scalars().first()

        if user:
            raise EmailInUseError

    await check_username(user_create.username)
    await check_email(user_create.email)

    hashed_password = None
    if user_create.password:
        hashed_password = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        email=user_create.email,
        username=user_create.username,
        password_hash=hashed_password,
        telegram=user_create.telegram,
    )

    db.add(new_user)
    await db.flush()
    await db.commit()

    user_scheme = UserScheme(**new_user.__dict__)

    return user_scheme


async def get(param, db: AsyncSession) -> UserScheme:
    if isinstance(param, int):
        query = select(User).filter(User.user_id == param)
    else:
        if re.match(settings.validation.email_pattern, param) is not None:
            query = select(User).filter(User.email == param)
        else:
            query = select(User).filter(User.username == param)

    result = await db.execute(query)

    user = result.scalars().first()

    if user:
        user_scheme = UserScheme(**user.__dict__)
        return user_scheme

    raise UserNotFoundError


async def check_password(user_id: int, db: AsyncSession) -> bool:
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        return user.password_hash is not None
    raise UserNotFoundError


async def get_hash(user_id: int, db: AsyncSession) -> bytes:
    query = select(User).filter(User.user_id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        return user.password_hash
    raise UserNotFoundError
