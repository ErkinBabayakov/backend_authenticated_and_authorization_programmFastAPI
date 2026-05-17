from pydantic import Field

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    password: str
    retry_password: str
    is_admin: bool = False


class UserAdd(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    is_active: bool = True
    hashed_password: str
    is_admin: bool = False


class UserEnter(BaseModel):
    email: EmailStr
    password: str


class UserDelete(BaseModel):
    email: EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class UserWithHashPassword(User):
    hashed_password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
