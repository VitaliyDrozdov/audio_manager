from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from src.auth.schemas import TokenData
from src.dependencies import get_current_user
from src.users.models import Roles


def roles_required(min_required_role: Roles):
    def _check_role(get_user: Annotated[TokenData, Depends(get_current_user)]):

        if get_user.role < min_required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )
        return get_user

    return _check_role
