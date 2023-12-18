from core.exceptions.base import CustomException
from fastapi import status


class PasswordDoesNotMatchException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = "USER__PASSWORD_DOES_NOT_MATCH"
    message = "password does not match"


class DuplicateEmailOrNicknameException(CustomException):
    code = status.HTTP_409_CONFLICT
    error_code = "USER__DUPLICATE_EMAIL_OR_NICKNAME"
    message = "duplicate email or nickname"


class UserNotFoundException(CustomException):
    code = status.HTTP_404_NOT_FOUND
    error_code = "USER__NOT_FOUND"
    message = "user not found"


class UserNotVerified(CustomException):
    code = status.HTTP_403_FORBIDDEN
    error_code = "USER__NOT_VERIFIED"
    message = "user not verified"


class UserAgeInvalid(CustomException):
    code = status.HTTP_409_CONFLICT
    error_code = "USER__AGE_INVALID"
    message = "user age invalid"