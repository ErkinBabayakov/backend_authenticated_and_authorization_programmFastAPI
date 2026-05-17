from fastapi import Depends, Request
from typing import Annotated

from src.exceptions import (
    NoAccessTokenHTTPException,
    IncorrectTokenException,
    IncorrectTokenHTTPException,
)
from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


# Зависимость для аутентификации и авторизации
def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise NoAccessTokenHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data.get("user_id", None)


UserIdDep = Annotated[int, Depends(get_current_user_id)]


# Зависимость для async_session_maker
async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
