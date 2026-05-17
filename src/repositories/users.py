from sqlalchemy import select, update
from pydantic import EmailStr

from sqlalchemy.exc import NoResultFound

from src.exceptions import (
    EmailNotRegisteredException,
    UserNotFoundException,
    UserNotEnoughRightsException,
    UserAlreadyDeleteException,
    ObjectNotFoundException,
    UserDoesNotExistException,
)
from src.repositories.base import BaseRepository
from src.models.users import UserOrm
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashPassword


class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_with_hash_password(self, email: EmailStr):
        try:
            query = select(self.model).filter_by(email=email)
            result = await self.session.execute(query)
            model = result.scalars().one()
        except NoResultFound as ex:
            raise EmailNotRegisteredException from ex
        return UserWithHashPassword.model_validate(model)

    async def delete_user(self, user_id: int) -> None:
        query = select(self.model.is_active).where(self.model.id == user_id)
        result = await self.session.execute(query)
        model = result.scalars().first()

        if model is None:
            raise ObjectNotFoundException
        if not model:
            raise UserNotFoundException
        await self.session.execute(
            update(self.model).where(self.model.id == user_id).values(is_active=False)
        )

    async def check_verify_active_user(self, email: EmailStr):
        try:
            query = select(self.model.is_active).filter(self.model.email == email)
            result = await self.session.execute(query)
            model = result.scalars().one()
            if not model:
                raise UserDoesNotExistException
        except NoResultFound as ex:
            raise UserAlreadyDeleteException from ex
        return model

    async def check_verify_admin_user(self, email: EmailStr):
        try:
            query = select(self.model.is_admin).filter(self.model.email == email)
            result = await self.session.execute(query)
            model = result.scalars().one()
            if not model:
                raise UserNotEnoughRightsException
        except NoResultFound as ex:
            raise EmailNotRegisteredException from ex

        return model
