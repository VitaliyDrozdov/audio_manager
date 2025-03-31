import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.client import YandexClient
from src.auth.schemas import TokenData, TokenSchema
from src.exceptions import (
    AuthenticationError,
    UserNotCorrectPasswordException,
    UserNotFoundError,
)
from src.settings import settings
from src.users.models import UserProfile
from src.users.service import bcrypt_context


@dataclass
class AuthService:
    yandex_client: YandexClient
    db_session: AsyncSession

    async def yandex_auth(self, code: str):
        pass

    def get_yandex_redirect_url(self):
        pass

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundError()
        if not bcrypt_context.verify(password, user.password_hash):
            logging.warning(
                f"Failed authentication attempt for email: {user.email}"
            )
            raise UserNotCorrectPasswordException()

    def generate_access_token(
        self, email: str, user_id: int, username: str, expires_delta: timedelta
    ) -> str:
        payload = {
            "sub": email,
            "user_id": str(user_id),
            "username": username,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(
            claims=payload, key=settings.SECRET_KEY, algorithm="HS256"
        )

    def verify_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
            user_id = payload.get("user_id")
            if user_id is not None:
                user_id = int(user_id)
            username: str = payload.get("username")
            return TokenData(user_id=user_id, username=username)
        except JWTError as e:
            logging.warning(f"Token verification failed: {str(e)}")
            raise AuthenticationError()

    async def authenticate_user(self, email: str, password: str):
        user = await self.db_session.scalar(
            select(UserProfile).where(UserProfile.email == email)
        )
        self._validate_auth_user(user, password)
        return user

    async def login(self, email: str, password: str) -> TokenSchema:
        user = await self.authenticate_user(email, password)
        access_token = self.generate_access_token(
            user_id=user.id,
            username=user.username,
            email=user.email,
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )
        return TokenSchema(
            user_id=user.id, access_token=access_token, token_type="bearer"
        )

    # def get_user_id_from_token(self, token: str) -> int:
    #     try:
    #         payload = jwt.decode(
    #             token=token, key=settings.SECRET_KEY, algorithms="HS256"
    #         )
    #     except JWTError:
    #         raise TokenNotCorrect()
    #     return payload["user_id"]
