import logging
from dataclasses import dataclass

import httpx

from src.auth.schemas import YandexUserData
from src.exceptions import YandexAuthenticationError
from src.settings import settings


@dataclass
class YandexClient:
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        try:
            access_token = await self._get_user_access_token(code=code)
            logging.info(f"Got Yandex access_token: {access_token}")

            user_info = await self.async_client.get(
                "https://login.yandex.ru/info?format=json",
                headers={"Authorization": f"OAuth {access_token}"},
            )
            return YandexUserData(
                **user_info.json(), access_token=access_token
            )
        except Exception as e:
            logging.error(f"Error request to Yandex API. Error: {str(e)}")
            raise YandexAuthenticationError(str(e))

    async def _get_user_access_token(self, code: str) -> str:
        response = await self.async_client.post(
            settings.YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_SECRET_KEY,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        logging.info(f"Got response from Yandex: {response.json()}")
        return response.json()["access_token"]
