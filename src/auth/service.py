import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.client import YandexClient
from src.auth.schemas import (
    BaseAuth,
    TokenData,
    TokenSchema,
    YandexAccessResponse,
)
from src.exceptions import (
    AuthenticationError,
    UserNotCorrectPasswordException,
    UserNotFoundError,
)
from src.settings import settings
from src.users.models import Roles, UserProfile
from src.users.schemas import UserCreateSchema
from src.users.service import UserService, bcrypt_context


@dataclass
class AuthService:
    yandex_client: YandexClient
    db_session: AsyncSession
    user_service: UserService

    def get_yandex_redirect_url(self):
        logging.info(f"yandex_redirect_url: {settings.yandex_redirect_url}")
        return settings.yandex_redirect_url

    @staticmethod
    def _validate_auth_user(user: UserProfile | None, password: str) -> None:
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
            "user_id": user_id,
            "username": username,
            "email": email,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(
            claims=payload,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def _verify_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            user_id: int = int(payload.get("user_id"))
            username: str = payload.get("username")
            email: str = payload.get("email")
            return TokenData(user_id=user_id, username=username, email=email)
        except ExpiredSignatureError:
            raise AuthenticationError("Token expired!")
        except JWTError as e:
            logging.warning(f"Token verification failed: {str(e)}")
            raise AuthenticationError(str(e))

    async def authenticate_user(self, email: str, password: str):
        user = await self.db_session.scalar(
            select(UserProfile).where(UserProfile.email == email)
        )
        self._validate_auth_user(user, password)
        return user

    async def login(
        self,
        form_data: BaseAuth,
    ) -> TokenSchema:
        user = await self.authenticate_user(
            form_data.email, form_data.password
        )

        self._validate_auth_user(user, form_data.password)
        access_token = self.generate_access_token(
            user_id=user.id,
            username=user.username,
            email=user.email,
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )
        return TokenSchema(
            user_id=int(user.id),
            access_token=access_token,
            token_type="bearer",
        )

    async def refresh_access_token(self, old_token: str) -> TokenSchema:
        token_data = self._verify_token(old_token)
        user = await self.db_session.scalar(
            select(UserProfile).where(
                UserProfile.id == int(token_data.user_id)
            )
        )
        if not user:
            raise UserNotFoundError(user_id=token_data.user_id)

        new_token = self.generate_access_token(
            email=user.email,
            user_id=user.id,
            username=user.username,
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )
        return TokenSchema(
            user_id=user.id, access_token=new_token, token_type="bearer"
        )

    async def yandex_auth(self, code: str):
        yandex_user_data = await self.yandex_client.get_user_info(code=code)
        user = await self.user_service.get_user_by_email(
            email=yandex_user_data.default_email
        )
        if user is not None:
            access_token = self.generate_access_token(
                user_id=user.id,
                username=user.username,
                email=user.email,
                expires_delta=timedelta(
                    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                ),
            )
            return YandexAccessResponse(
                user_id=user.id,
                access_token=access_token,
                username=user.username,
                email=user.email,
            )

        create_user = UserCreateSchema(
            first_name="",
            last_name="",
            email=yandex_user_data.default_email,
            username=yandex_user_data.name,
            password="",
            role=Roles.SIMPLE_USER,
        )
        created_user = await self.user_service.create_user(create_user)
        access_token = self.generate_access_token(
            user_id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

        return YandexAccessResponse(
            user_id=created_user.id,
            access_token=access_token,
            username=create_user.username,
            email=create_user.email,
        )
