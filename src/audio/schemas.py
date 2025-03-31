from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel, field_validator

ALLOWED_EXTENSIONS = {"mp3", "wav", "flac", "ogg"}


class FileBase(BaseModel):
    filename: str
    description: str


class FileCreateSchema(FileBase):
    file: UploadFile
    owner_id: int

    @field_validator("file", mode="after")
    @classmethod
    def validate_file_extension(cls, value):
        if value.filename:
            extension = value.filename.split(".")[-1].lower()
            if extension not in ALLOWED_EXTENSIONS:
                raise ValueError(
                    "Invalid file type. Only audio files are allowed."
                )
        return value


class FileResponseSchema(FileBase):
    id: int
    filepath: str
    created_at: datetime
    updated_at: datetime | None = None

    # class Config:
    #     orm_mode = True
