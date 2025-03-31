from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.dependencies import get_user_service
from src.users.schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(body)


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
)
async def get_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
):
    return await user_service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponseSchema,
)
async def update_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    body: UserUpdateSchema,
    user_id: int,
):
    return await user_service.update_user(user_id=user_id, user_update=body)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_id: int,
):
    return await user_service.delete_user(user_id)
