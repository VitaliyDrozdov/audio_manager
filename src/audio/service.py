import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from fastapi import UploadFile
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.audio.models import AudioFile
from src.audio.schemas import FileCreateSchema
from src.settings import settings
from src.users.models import UserProfile
from src.users.service import UserService


@dataclass
class AudiFileService:
    db_session: AsyncSession
    user_service: UserService
    # cache: FileCacheRepository

    @staticmethod
    def _create_dir():
        if not os.path.exists(settings.FILE_UPLOAD_DIRECTORY):
            os.makedirs(settings.FILE_UPLOAD_DIRECTORY)

    async def get_all_files(self) -> Sequence[AudioFile]:
        res = await self.db_session.scalars(
            select(AudioFile).options(
                joinedload(AudioFile.owner).load_only(
                    UserProfile.id, UserProfile.email, UserProfile.username
                )
            )
        )
        # return [
        #     FileResponseSchema.model_validate(file, from_attributes=True)
        #     for file in res.all()
        # ]
        return res.all()

    async def upload_file(
        self, file_upload: FileCreateSchema, file: UploadFile
    ):
        await self.user_service.get_user_by_id(file_upload.owner_id)
        data = file_upload.model_dump(exclude_none=True)
        data["created_at"] = datetime.now(timezone.utc)
        self._create_dir()
        path_ = os.path.join(
            settings.FILE_UPLOAD_DIRECTORY, file_upload.filename
        )
        content = await file.read()
        with open(path_, "wb") as f_write:
            f_write.write(content)
        try:
            res = await self.db_session.scalar(
                insert(AudioFile).values(**data)
            )
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            logging.error(
                f"Failed to create AudiFile row: {file_upload.filename}. "
                f"Error: {str(e)}"
            )
            raise
        data["id"] = res.id
        # return FileResponseSchema(**data)
        return res

    async def get_files_by_user(self, user_id: int) -> Sequence[AudioFile]:
        await self.user_service.get_user_by_id(user_id)
        res = await self.db_session.scalars(
            select(AudioFile)
            .options(
                joinedload(AudioFile.owner).load_only(
                    UserProfile.id, UserProfile.email, UserProfile.username
                )
            )
            .where(AudioFile.owner_id == user_id)
        )
        # return [
        #     FileResponseSchema.model_validate(file, from_attributes=True)
        #     for file in res.all()
        # ]
        return res.all()
