from pydantic import BaseModel, EmailStr, Field

from src.users.models import Roles


class TokenSchema(BaseModel):
    user_id: int
    access_token: str
    token_type: str = Field(default="bearer")
    role: Roles | None = Roles.SIMPLE_USER


class TokenData(BaseModel):
    user_id: int | None = None
    username: str | None = None
    email: str | None = None
    role: int | None = Roles.SIMPLE_USER


class YandexUserData(BaseModel):
    id: int
    login: str
    name: str = Field(alias="real_name")
    default_email: str
    access_token: str


class YandexAccessResponse(TokenSchema):
    username: str | None = None
    email: str | None = None


class OauthRefresh(BaseModel):
    email: EmailStr


class BaseAuth(BaseModel):
    email: EmailStr
    password: str
    username: str
