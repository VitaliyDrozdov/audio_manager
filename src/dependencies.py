from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db_accessor import DBSession
from src.users.service import UserService


async def get_user_service(
    db_session: AsyncSession = Depends(DBSession),
) -> UserService:
    return UserService(db_session=db_session)
