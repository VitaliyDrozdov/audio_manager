from datetime import datetime

from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str
    owner_id: int
    description: str


class FileCreateSchema(FileBase):
    pass


class FileResponseSchema(FileBase):
    id: int
    filepath: str
    created_at: datetime
    updated_at: datetime | None = None
