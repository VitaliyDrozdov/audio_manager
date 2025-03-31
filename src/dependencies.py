from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.audio.service import AudiFileService
from src.infra.db_accessor import db_config
from src.users.service import UserService


async def get_user_service(
    db_session: AsyncSession = Depends(db_config.get_db),
) -> UserService:
    return UserService(db_session=db_session)


async def get_audio_service(
    db_session: AsyncSession = Depends(db_config.get_db),
    user_service: UserService = Depends(get_user_service),
) -> AudiFileService:
    return AudiFileService(db_session=db_session, user_service=user_service)
