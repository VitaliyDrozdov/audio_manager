import logging
from dataclasses import dataclass

import httpx

from src.auth.schemas import YandexUserData
from src.settings import settings


@dataclass
class YandexClient:
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self._get_user_access_token(code=code)
        logging.debug(f"access_token: {access_token}")
        async with self.async_client as client:
            user_info = await client.get(
                "https://login.yandex.ru/info?format=json",
                headers={"Authorization": f"OAuth {access_token}"},
            )
        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        async with self.async_client as client:
            response = await client.post(
                settings.YANDEX_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": settings.YANDEX_CLIENT_ID,
                    "client_secret": settings.YANDEX_SECRET_KEY,
                    # 'redirect_uri':
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            logging.debug(f"response: {response.json()}")
        return response.json()["access_token"]
