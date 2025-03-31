from fastapi import HTTPException, status


# TODO: добавить обычные исклюючения(не http) для сервисного слоя
class UserError(HTTPException):
    """Base exception for user-related errors"""

    pass


class UserAlreadyExists(UserError):
    def __init__(self, email=None, username=None):
        message = (
            "User already exists"
            if email is None and username is None
            else f"User with email '{email}', username '{username}' already exists"  # noqa E501
        )
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=message
        )


class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = (
            "User not found"
            if user_id is None
            else f"User with id {user_id} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
