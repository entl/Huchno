from core.exceptions.base import CustomException


class TokenException(CustomException):
    pass


class DecodeTokenException(TokenException):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(TokenException):
    code = 400
    error_code = "TOKEN__EXPIRE_ERROR"
    message = "expired token"