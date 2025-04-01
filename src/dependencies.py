from typing import Annotated

import httpx
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.audio.service import AudiFileService
from src.auth.client import YandexClient
from src.auth.schemas import TokenData
from src.auth.service import AuthService
from src.infra.db_accessor import db_config
from src.users.service import UserService

reusable_oauth2 = HTTPBearer()
Token = Annotated[HTTPAuthorizationCredentials, Security(reusable_oauth2)]


async def get_user_service(
    db_session: AsyncSession = Depends(db_config.get_db),
) -> UserService:
    """Dependency to provide a UserService instance."""
    return UserService(db_session=db_session)


async def get_audio_service(
    db_session: Annotated[AsyncSession, Depends(db_config.get_db)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AudiFileService:
    """Dependency to provide an AudiFileService instance."""
    return AudiFileService(db_session=db_session, user_service=user_service)


async def get_async_client() -> httpx.AsyncClient:
    """Provides an HTTP client for async requests."""
    return httpx.AsyncClient()


async def get_yandex_client(
    async_client: Annotated[httpx.AsyncClient, Depends(get_async_client)],
) -> YandexClient:
    """Dependency to provide a YandexClient instance."""
    return YandexClient(async_client=async_client)


async def get_auth_service(
    db_session: Annotated[AsyncSession, Depends(db_config.get_db)],
    yandex_client: Annotated[YandexClient, Depends(get_yandex_client)],
    user_serivce: Annotated[UserService, Depends(get_user_service)],
) -> AuthService:
    """Dependency to provide an AuthService instance."""
    return AuthService(
        db_session=db_session,
        yandex_client=yandex_client,
        user_service=user_serivce,
    )


async def get_current_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> TokenData:
    """Retrieves the currently authenticated user from the token."""
    return auth_service._verify_token(token.credentials)
