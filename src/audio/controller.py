from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from src.audio.schemas import FileCreateSchema, FileResponseSchema
from src.audio.service import AudiFileService
from src.dependencies import get_audio_service

router = APIRouter(prefix="/audios", tags=["Audios"])


@router.post(
    "/", response_model=FileResponseSchema, status_code=status.HTTP_201_CREATED
)
async def upload_audio(
    body: FileCreateSchema,
    audio_service: Annotated[AudiFileService, Depends(get_audio_service)],
    file: UploadFile = File(...),
):
    return await audio_service.upload_file(file_upload=body, file=file)
