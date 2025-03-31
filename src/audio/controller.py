from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import ValidationError

from src.audio.schemas import FileCreateSchema, FileResponseSchema
from src.audio.service import AudiFileService
from src.dependencies import get_audio_service, get_current_user
from src.exceptions import FileNotSupported

router = APIRouter(
    prefix="/audios",
    tags=["Audios"],
    dependencies=[Depends(get_current_user)],
)


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
    try:
        file_data = FileCreateSchema(
            filename=filename,
            owner_id=owner_id,
            description=description,
            file=file,
        )
    except ValidationError:
        # TODO: перенести в сервис
        raise FileNotSupported()

    return await audio_service.upload_file(file_upload=file_data, file=file)


@router.get("/{user_id}/files", response_model=list[FileResponseSchema])
async def get_files_by_user_id(
    audio_service: Annotated[AudiFileService, Depends(get_audio_service)],
    user_id: int,
):

    return await audio_service.get_files_by_user(
        user_id=user_id,
    )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    audio_service: Annotated[AudiFileService, Depends(get_audio_service)],
    file_id: int,
):
    return await audio_service.delete_file(file_id)
