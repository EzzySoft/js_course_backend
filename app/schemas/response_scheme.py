from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    message: str = None


class SuccessResponse(BaseModel):
    status: str = "ok"
    detail: Any = None


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: Message
