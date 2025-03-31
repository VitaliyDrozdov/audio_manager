from pydantic import BaseModel, EmailStr

from src.users.models import Roles


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: Roles


class UserCreateSchema(UserBase):
    password: str


class UserResponseSchema(UserBase):
    id: int
