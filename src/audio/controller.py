from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from src.audio.schemas import FileCreateSchema, FileResponseSchema
from src.audio.service import AudiFileService
from src.dependencies import get_audio_service

router = APIRouter(prefix="/audios", tags=["Audios"])


@router.post(
    "/", response_model=FileResponseSchema, status_code=status.HTTP_201_CREATED
)
async def upload_audio(
    audio_service: Annotated[AudiFileService, Depends(get_audio_service)],
    filename: Annotated[str, Form()],
    owner_id: Annotated[int, Form()],
    description: Annotated[str, Form()],
    file: UploadFile = File(...),
):
    file_data = FileCreateSchema(
        filename=filename, owner_id=owner_id, description=description
    )
    return await audio_service.upload_file(file_upload=file_data, file=file)
