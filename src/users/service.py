import logging
from dataclasses import dataclass

from passlib.context import CryptContext
from sqlalchemy import insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

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
            raise ValueError("email or username already exist")
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
                f"Failed to register user: {user_create.email}. "
                f"Error: {str(e)}"
            )
            raise
        user_create_data["id"] = res.scalar()
        return UserResponseSchema(**user_create_data)
