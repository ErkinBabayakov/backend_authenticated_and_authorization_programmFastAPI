from fastapi import APIRouter, Response, Query

from src.exceptions import (
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    UserNotFoundHTTPException,
    UserNotFoundException,
    UserDoesNotExistException,
    UserDoesNotExistHTTPException,
    IncorrectPasswordRetryException,
    IncorrectPasswordRetryHTTPException,
    UserNotEnoughRightsException,
    UserNotEnoughRightsHTTPException,
    UserAlreadyDeleteException,
    UserAlreadyDeleteHTTPException,
)
from src.services.auth import AuthService
from src.schemas.users import UserRequestAdd, UserEnter, UserUpdate, UserDelete
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация пользователя"])


@router.post(
    "/register",
    summary="Создать пользователя",
    description="Нажмите кнопку Try it out, заполните поля и нажмите execute",
)
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    except IncorrectPasswordRetryException:
        raise IncorrectPasswordRetryHTTPException

    return "Вы создали нового пользователя"


@router.post("/login", summary="Войти", description="Введите валидный email и пароль")
async def login_user(
    db: DBDep,
    data: UserEnter,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    except UserDoesNotExistException:
        raise UserDoesNotExistHTTPException

    response.set_cookie("access_token", access_token)
    return "Вы успешно зашли в систему"


@router.get(
    "/me", summary="Мой профиль", description="Получить информацию о своем профиле"
)
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        return await AuthService(db).get_me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.patch(
    "/{user_id}",
    summary="Обновить информацию о пользователе",
    description="Введите ваш user_id и заполните поля, которые вы хотите изменить",
)
async def update_user(db: DBDep, user_id: int, user_data: UserUpdate):
    try:
        await AuthService(db).partial_update_user(user_id, user_data)
        return "Пользователь обновлен"
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    except UserDoesNotExistException:
        raise UserDoesNotExistHTTPException


@router.post("/logout", summary="Выйти")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return "Вы вышли из системы"


@router.delete(
    "/{user_id}",
    summary="Удаляем пользователя по его user_id",
    description="Введите user_id удаляемого пользователя и ваш email",
)
async def delete_user(
    db: DBDep,
    user_id: int,
    response: Response,
    user_data: UserDelete = Query(),
):
    try:
        await AuthService(db).delete_user(user_id, user_data)
        response.delete_cookie("access_token")
        return "Вы успешно удалили пользователя"
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except UserNotEnoughRightsException:
        raise UserNotEnoughRightsHTTPException
    except UserAlreadyDeleteException:
        raise UserAlreadyDeleteHTTPException
    except UserDoesNotExistException:
        raise UserDoesNotExistHTTPException
