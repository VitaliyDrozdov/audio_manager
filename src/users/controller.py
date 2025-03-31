from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.dependencies import get_user_service
from src.users.schemas import UserCreateSchema, UserResponseSchema
from src.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(user_create=body)
