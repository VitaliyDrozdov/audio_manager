from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


class DBConfig:
    def __init__(self):
        self.DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"  # noqa E501
        self.engine = create_async_engine(self.DATABASE_URL, echo=True)
        self.AsyncSession_ = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.AsyncSession_() as session:
            yield session


db_config = DBConfig()
# DBSession = Annotated[AsyncSession, Depends(db_config.get_db)]


class Base(DeclarativeBase):
    pass
