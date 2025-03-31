import logging
from dataclasses import dataclass

from passlib.context import CryptContext
from sqlalchemy import insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import UserAlreadyExists, UserNotFoundError
from src.users.models import UserProfile
from src.users.schemas import UserCreateSchema, UserResponseSchema

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class UserService:
    db_session: AsyncSession
    # auth_service: AuthService

    async def create_user(
        self, user_create: UserCreateSchema
    ) -> UserResponseSchema:
        existing_user = await self.db_session.scalar(
            select(UserProfile).where(
                or_(
                    UserProfile.email == user_create.email,
                    UserProfile.username == user_create.username,
                )
            )
        )
        if existing_user:
            logging.warning(
                f"Attempted to create existing user: "
                f"{user_create.email} {user_create.username}"
            )
            raise UserAlreadyExists(
                email=user_create.email, username=user_create.username
            )
        user_create_data = user_create.model_dump(
            exclude_none=True, exclude={"password"}
        )
        user_create_data["password_hash"] = bcrypt_context.hash(
            user_create.password
        )
        try:
            res = await self.db_session.execute(
                insert(UserProfile)
                .values(**user_create_data)
                .returning(UserProfile.id)
            )
            # await self.db_session.flush()
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

    async def get_user_by_id(self, user_id: int) -> UserResponseSchema:
        user = await self.db_session.scalar(
            select(UserProfile).where(UserProfile.id == user_id)
        )
        if not user:
            logging.warning(f"User not found with ID: {user_id}")
            raise UserNotFoundError(user_id)
        logging.info(f"Successfully retrieved user with ID: {user_id}")
        return user
