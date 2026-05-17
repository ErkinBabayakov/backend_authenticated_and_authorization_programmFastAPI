from fastapi import HTTPException


class AuthenticatedAndAuthorizationServiceException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectAlreadyExistsException(AuthenticatedAndAuthorizationServiceException):
    detail = "Объект уже существует"


class ObjectNotFoundException(AuthenticatedAndAuthorizationServiceException):
    detail = "Объект не найден"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class EmailNotRegisteredException(AuthenticatedAndAuthorizationServiceException):
    detail = "Пользователь с таким email не зарегистрирован"


class UserAlreadyExistsException(AuthenticatedAndAuthorizationServiceException):
    detail = "Пользователь с таким email уже сущесвует"


class IncorrectTokenException(AuthenticatedAndAuthorizationServiceException):
    detail = "Неверный токен"


class IncorrectPasswordException(AuthenticatedAndAuthorizationServiceException):
    detail = "Неверный пароль"


class IncorrectPasswordRetryException(AuthenticatedAndAuthorizationServiceException):
    detail = "Пароли должны совпадать"


class UserDoesNotExistException(AuthenticatedAndAuthorizationServiceException):
    detail = "Вы не можете удалять или обновлять пользователей, т.к. ваш акаунт был удален или заблокирован ранее"


class UserNotEnoughRightsException(AuthenticatedAndAuthorizationServiceException):
    detail = "Нет прав"


class UserAlreadyDeleteException(AuthenticatedAndAuthorizationServiceException):
    detail = "Пользователь был удален"


class UserDoesNotUpdateException(AuthenticatedAndAuthorizationServiceException):
    detail = "Вы не можете обновить пользовтеля, т.к. ваш акаунт был удален"


class AuthenticatedAndAuthorizationServiceHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFoundHTTPException(AuthenticatedAndAuthorizationServiceHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class IncorrectTokenHTTPException(AuthenticatedAndAuthorizationServiceHTTPException):
    status_code = 401
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(
    AuthenticatedAndAuthorizationServiceHTTPException
):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(
    AuthenticatedAndAuthorizationServiceHTTPException
):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class IncorrectPasswordHTTPException(AuthenticatedAndAuthorizationServiceHTTPException):
    status_code = 401
    detail = "Неверный пароль"


class IncorrectPasswordRetryHTTPException(
    AuthenticatedAndAuthorizationServiceHTTPException
):
    status_code = 401
    detail = "Вводимые пароли должны совпадать"


class NoAccessTokenHTTPException(AuthenticatedAndAuthorizationServiceHTTPException):
    status_code = 401
    detail = "Вы не прошли аутентификацию"


class UserDoesNotExistHTTPException(AuthenticatedAndAuthorizationServiceHTTPException):
    status_code = 403
    detail = "Вы не можете удалять или обновлять пользователей, т.к. ваш акаунт был удален или заблокирован ранее"


class UserNotEnoughRightsHTTPException(
    AuthenticatedAndAuthorizationServiceHTTPException
):
    status_code = 403
    detail = "У вас нет прав на удаление пользователей"


class UserAlreadyDeleteHTTPException(AuthenticatedAndAuthorizationServiceHTTPException):
    status_code = 409
    detail = "Ошибка. Пользователь был удален ранее"


class UserDoesNotUpdateHTTPException(AuthenticatedAndAuthorizationServiceHTTPException):
    status_code = 403
    detail = "Вы не можете обновить пользовтеля, т.к. ваш акаунт был удален"
