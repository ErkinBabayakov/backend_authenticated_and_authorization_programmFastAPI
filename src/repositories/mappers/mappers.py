from src.repositories.mappers.base import DataMapper
from src.models.users import UserOrm
from src.schemas.users import User


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = User
