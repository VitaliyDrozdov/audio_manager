from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str
    filepath: str
    owner_id: int
    description: str


class FileCreate(FileBase):
    pass


class FileResponse(FileBase):
    id: int
    updated_at: str
