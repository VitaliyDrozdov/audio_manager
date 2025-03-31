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


class FileError(HTTPException):
    """Base exception for user-related errors"""

    pass


class FileNotSupported(FileError):
    def __init__(self, extension=None):
        message = (
            "Only audio files allowed"
            if extension is None
            else f"Extension '{extension}' not supported"
        )
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message
        )


class FileNotFoundError_(FileError):
    def __init__(self, file_id=None):
        message = (
            "file not found"
            if file_id is None
            else f"file with id {file_id} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"


class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Could not validate user"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=message
        )
