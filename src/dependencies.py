from typing import Annotated

import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.audio.service import AudiFileService
from src.auth.client import YandexClient
from src.auth.schemas import TokenData
from src.auth.service import AuthService, oauth2_scheme
from src.infra.db_accessor import db_config
from src.users.service import UserService


async def get_user_service(
    db_session: AsyncSession = Depends(db_config.get_db),
) -> UserService:
    return UserService(db_session=db_session)


async def get_audio_service(
    db_session: Annotated[AsyncSession, Depends(db_config.get_db)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AudiFileService:
    return AudiFileService(db_session=db_session, user_service=user_service)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_yandex_client(
    async_client: Annotated[httpx.AsyncClient, Depends(get_async_client)],
) -> YandexClient:
    return YandexClient(async_client=async_client)


async def get_auth_service(
    db_session: Annotated[AsyncSession, Depends(db_config.get_db)],
    yandex_client: Annotated[YandexClient, Depends(get_yandex_client)],
) -> AuthService:
    return AuthService(db_session=db_session, yandex_client=yandex_client)


async def get_current_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    return auth_service._verify_token(token)
