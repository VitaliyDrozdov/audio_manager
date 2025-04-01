import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Sequence

from fastapi import UploadFile
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.audio.models import AudioFile
from src.audio.schemas import FileCreateSchema, FileResponseSchema
from src.exceptions import FileNotFoundError_
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
        """
        Creates the directory for file uploads if it does not already exist.
        """
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
        """
        Uploads an audio file with specified filename, stores it in the system,
        and saves its metadata to the database.
        """
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
        """
        Retrieves all audio files associated with a specific user.
        """
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

    async def get_file_by_id(self, file_id: int) -> AudioFile:
        """
        Retrieves a specific audio file by its ID.
        """
        file = await self.db_session.scalar(
            select(AudioFile).where(AudioFile.id == file_id)
        )
        if not file:
            logging.warning(f"file not found with ID: {file_id}")
            raise FileNotFoundError_(file_id)
        logging.info(f"Successfully retrieved file with ID: {file_id}")
        return file

    async def delete_file(self, file_id: int) -> None:
        file = await self.get_file_by_id(file_id)
        try:
            res = await self.db_session.execute(
                delete(AudioFile).where(AudioFile.id == file_id)
            )
            await self.db_session.commit()
            if res.rowcount == 0:
                logging.error(
                    f"file '{file_id}' was not deleted. res.rowcount != 0"
                )
                raise ValueError()
        except Exception as e:
            await self.db_session.rollback()
            logging.error(
                f"Failed to delete file: {file.id}. " f"Error: {str(e)}"
            )
            raise
