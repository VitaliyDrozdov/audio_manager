import logging
from dataclasses import dataclass

from passlib.context import CryptContext
from sqlalchemy import delete, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import UserAlreadyExists, UserNotFoundError
from src.users.models import UserProfile
from src.users.schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class UserService:
    db_session: AsyncSession
    # auth_service: AuthService

    async def _check_unique_user(self, email, username):
        existing_user = await self.db_session.scalar(
            select(UserProfile).where(
                or_(
                    UserProfile.email == email,
                    UserProfile.username == username,
                )
            )
        )
        if existing_user:
            logging.warning(
                f"Attempted to create existing user: " f"{email} {username}"
            )
            raise UserAlreadyExists(email=email, username=username)

    async def create_user(
        self, user_create: UserCreateSchema
    ) -> UserResponseSchema:
        await self._check_unique_user(user_create.email, user_create.username)
        user_create_data = user_create.model_dump(
            exclude_none=True, exclude={"password"}
        )
        if user_create.password:
            user_create_data["password_hash"] = bcrypt_context.hash(
                user_create.password
            )
        try:
            res = await self.db_session.execute(
                insert(UserProfile)
                .values(**user_create_data)
                .returning(UserProfile.id)
            )
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            logging.error(
                f"Failed to create user: {user_create.email}. "
                f"Error: {str(e)}"
            )
            raise
        user_create_data["id"] = res.scalar()
        return UserResponseSchema(**user_create_data)

    async def get_user_by_id(self, user_id: int) -> UserProfile:
        user = await self.db_session.scalar(
            select(UserProfile).where(UserProfile.id == user_id)
        )
        if not user:
            logging.warning(f"User not found with ID: {user_id}")
            raise UserNotFoundError(user_id)
        logging.info(f"Successfully retrieved user with ID: {user_id}")
        return user

    async def get_user_by_email(self, email: str) -> UserProfile:
        user = await self.db_session.scalar(
            select(UserProfile).where(UserProfile.email == email)
        )
        if not user:
            return None
        #     logging.warning(f"User not found with email: {email}")
        #     raise UserNotFoundError(email)
        logging.info(f"Successfully retrieved user with email: {email}")
        return user

    async def update_user(
        self, user_update: UserUpdateSchema, user_id: int
    ) -> UserResponseSchema:
        user = await self.get_user_by_id(user_id)
        user_update_data = user_update.model_dump(
            exclude_none=True,
        )
        for k, v in user_update_data.items():
            setattr(user, k, v)
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            logging.error(
                f"Failed to update user: {user.email}. " f"Error: {str(e)}"
            )
            raise
        return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        try:
            res = await self.db_session.execute(
                delete(UserProfile).where(UserProfile.id == user_id)
            )
            await self.db_session.commit()
            if res.rowcount == 0:
                logging.error(
                    f"User '{user_id}' was not deleted. res.rowcount != 0"
                )
                raise ValueError()
        except Exception as e:
            await self.db_session.rollback()
            logging.error(
                f"Failed to delete user: {user.email}. " f"Error: {str(e)}"
            )
            raise
