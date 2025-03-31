import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from src.auth.schemas import (
    BaseAuth,
    TokenData,
    TokenSchema,
    YandexAccessResponse,
)
from src.auth.service import AuthService
from src.dependencies import (
    Token,
    get_auth_service,
    get_current_user,
    get_user_service,
)
from src.users.schemas import UserResponseSchema
from src.users.service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenSchema)
async def login(
    form_data: BaseAuth,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.login(form_data)


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Token,
    current_user: Annotated[TokenData, Depends(get_current_user)],
):

    return await auth_service.refresh_access_token(token.credentials)


@router.get("/me", response_model=UserResponseSchema)
async def me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    return await user_service.get_user_by_id(current_user.user_id)


@router.get("/yandex/redirect", response_class=RedirectResponse)
async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_yandex_redirect_url()
    return RedirectResponse(redirect_url)


@router.get("/yandex/callback", response_model=YandexAccessResponse)
async def yandex_callback(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str,
):
    logging.info(f"Yandex access token: {code}")
    return await auth_service.yandex_auth(code)
