from dataclasses import dataclass

# from src.users.models import
from src.auth.client import YandexClient

# from src.exceptions import (
#     TokenExpired,
#     TokenNotCorrect,
#     UserNotCorrectPasswordException,
# )
from src.settings import settings as settings_

# from src.users.models import UserProfile

# from datetime import datetime as dt
# from datetime import timedelta

# from jose import JWTError, jwt


@dataclass
class AuthService:
    settings: settings_
    yandex_client: YandexClient

    async def yandex_auth(self, code: str):
        pass

    def get_yandex_redirect_url(self):
        pass
