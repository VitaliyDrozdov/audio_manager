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
from src.audio.schemas import FileCreateSchema, FileResponseSchema
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

        return res.all()

    async def upload_file(
        self, file_upload: FileCreateSchema, file: UploadFile
    ) -> FileResponseSchema:
        await self.user_service.get_user_by_id(file_upload.owner_id)

        data = file_upload.model_dump(exclude_none=True, exclude={"file"})
        data["created_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
        extension = file.filename.split(".")[-1].lower()

        self._create_dir()
        path_ = os.path.join(
            settings.FILE_UPLOAD_DIRECTORY,
            f"{file_upload.filename}.{extension}",
        )
        absolute_path = os.path.abspath(path_)
        content = await file.read()
        with open(path_, "wb") as f_write:
            f_write.write(content)
        try:
            data["filepath"] = absolute_path
            res = await self.db_session.execute(
                insert(AudioFile).values(**data).returning(AudioFile.id)
            )
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            logging.error(
                f"Failed to create AudiFile row: {file_upload.filename}. "
                f"Error: {str(e)}"
            )
            raise
        data["id"] = res.scalar()
        return FileResponseSchema(**data)

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

        return res.all()
