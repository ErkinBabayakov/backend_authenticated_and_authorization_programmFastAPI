import jwt

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.config import settings
from src.schemas.users import UserRequestAdd, UserAdd, UserUpdate, UserEnter, UserDelete
from src.services.base import BaseService
from sqlalchemy.exc import IntegrityError
from src.exceptions import (
    IncorrectTokenException,
    EmailNotRegisteredException,
    IncorrectPasswordException,
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    ObjectNotFoundException,
    UserNotFoundException,
    UserDoesNotExistException,
    IncorrectPasswordRetryException,
    UserNotEnoughRightsException,
    UserAlreadyDeleteHTTPException,
    UserDoesNotExistHTTPException,
)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
        if data.password != data.retry_password:
            raise IncorrectPasswordRetryException
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password=hashed_password,
            is_admin=data.is_admin,
        )
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserEnter):
        query = await self.db.users.check_verify_active_user(data.email)
        if not query:
            raise UserDoesNotExistException

        user = await self.db.users.get_user_with_hash_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_me(self, user_id: int):
        try:
            user = await self.db.users.get_one(id=user_id)
            return user
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex

    async def partial_update_user(self, user_id: int, user_data: UserUpdate):
        try:
            query_is_active = await self.db.users.check_verify_active_user(
                user_data.email
            )
            if not query_is_active:
                raise UserDoesNotExistException
            updated_user = await self.db.users.edit(
                user_data, id=user_id, exclude_unset=True
            )
            await self.db.commit()
            return updated_user
        except IntegrityError as ex:
            raise UserAlreadyExistsException from ex

    async def delete_user(self, user_id: int, user_data: UserDelete):
        try:
            query_verify_admin = await self.db.users.check_verify_admin_user(
                user_data.email
            )
            if not query_verify_admin:
                raise UserNotEnoughRightsException
            query_is_active = await self.db.users.check_verify_active_user(
                user_data.email
            )
            if not query_is_active:
                raise UserDoesNotExistException
            await self.db.users.delete_user(user_id=user_id)
            await self.db.commit()
        except UserNotFoundException as ex:
            raise UserAlreadyDeleteHTTPException from ex
        except ObjectNotFoundException as ex:
            raise EmailNotRegisteredException from ex
        except UserDoesNotExistException as ex:
            raise UserDoesNotExistHTTPException from ex
