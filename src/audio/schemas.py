from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str
    filepath: str
    owner_id: int
    description: str


class FileCreateSchema(FileBase):
    pass


class FileResponseSchema(FileBase):
    id: int
    created_at: str
    updated_at: str
