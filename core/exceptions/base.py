from http import HTTPStatus
from fastapi import HTTPException, status


class CustomException(Exception):
    code = status.HTTP_502_BAD_GATEWAY
    error_code = status.HTTP_502_BAD_GATEWAY
    message = status.HTTP_502_BAD_GATEWAY

    def __init__(self, message=None):
        if message:
            self.message = message


class BadRequestException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DatabaseException(CustomException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = HTTPStatus.INTERNAL_SERVER_ERROR.description
