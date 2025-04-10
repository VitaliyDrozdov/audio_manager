from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import ValidationError

from src.audio.schemas import FileCreateSchema, FileResponseSchema
from src.audio.service import AudiFileService
from src.auth.schemas import TokenData
from src.dependencies import get_audio_service, get_current_user
from src.exceptions import FileNotSupported
from src.permissions import roles_required
from src.users.models import Roles

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
    current_user: Annotated[TokenData, Depends(get_current_user)],
    description: Annotated[str, Form()],
    file: UploadFile = File(...),
):
    try:
        file_data = FileCreateSchema(
            filename=filename,
            owner_id=current_user.user_id,
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
    current_user: Annotated[
        TokenData, Depends(roles_required(Roles.SUPERUSER))
    ],
):
    return await audio_service.delete_file(file_id)
