from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


class DBConfig:
    """Handles database configuration and provides async session management."""

    DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"  # noqa E501
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSession_ = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Provides an async database session."""
        async with self.AsyncSession_() as session:
            yield session


db_config = DBConfig()


class Base(DeclarativeBase):
    pass
