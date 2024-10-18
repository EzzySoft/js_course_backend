from typing import Optional
from pydantic import BaseModel, EmailStr


class CredentialsScheme(BaseModel):
    login: str
    password: str


class CreateUserScheme(BaseModel):
    email: EmailStr
    username: str
    password: str = None
    telegram: str


class UserScheme(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    password_hash: Optional[bytes] = None
    telegram: str


class UserGetScheme(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    telegram: str
