from pydantic import BaseModel, EmailStr

from src.users.models import Roles


class UserBase(BaseModel):
    first_name: str | None
    last_name: str | None
    role: Roles | None


class UserUpdateSchema(UserBase):
    pass


class UserCreateSchema(UserBase):
    email: EmailStr
    username: str
    password: str


class UserResponseSchema(UserBase):
    email: EmailStr
    username: str
    id: int
