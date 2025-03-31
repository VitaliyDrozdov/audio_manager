from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.auth.schemas import TokenSchema
from src.auth.service import AuthService
from src.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: str = Depends(oauth2_scheme),
):
    return await auth_service.refresh_access_token(token)
