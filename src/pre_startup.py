import logging

from fastapi import FastAPI
from sqlalchemy import select

from src.infra.db_accessor import db_config
from src.settings import settings
from src.users.models import Roles, UserProfile
from src.users.service import bcrypt_context


async def create_superuser(app: FastAPI):
    """
    Creates a superuser if one does not exist. This function checks if
    a superuser exists by querying the database. If not, it creates a new
    superuser with the credentials provided in the settings.
    """
    async with db_config.AsyncSession_() as session:
        superuser = await session.execute(
            select(UserProfile).where(UserProfile.role == Roles.SUPERUSER)
        )
        superuser = superuser.scalars().first()
        if superuser:
            logging.warning(f"Superuser exists: '{superuser.email}'")
            return
        else:
            new_superuser = UserProfile(
                email=settings.SUPERUSER_EMAIL,
                username=settings.SUPERUSER_USERNAME,
                password_hash=bcrypt_context.hash(settings.SUPERUSER_PASSWORD),
                role=Roles.SUPERUSER,
            )
            session.add(new_superuser)
            await session.commit()
            await session.refresh(new_superuser)
            logging.info(
                f"Superuser created. email: '{new_superuser.email}', username: '{new_superuser.username}'"  # noqa E501
            )
