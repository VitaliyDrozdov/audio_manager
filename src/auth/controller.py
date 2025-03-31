from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.schemas import TokenData, TokenSchema
from src.auth.service import AuthService
from src.dependencies import (
    get_auth_service,
    get_current_user,
    get_user_service,
)
from src.users.schemas import UserResponseSchema
from src.users.service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenSchema)
async def login(
    # body: UserCreateSchema,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.login(form_data)


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/token")),
):
    return await auth_service.refresh_access_token(token)


@router.get("/me", response_model=UserResponseSchema)
async def me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    return await user_service.get_user_by_id(current_user.user_id)
