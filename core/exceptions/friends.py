from core.exceptions.base import CustomException


class AlreadySentRequest(CustomException):
    code = 409
    error_code = "REQUEST__SEND_ERROR"
    message = "already sent request"


class AlreadyReceivedRequest(CustomException):
    code = 409
    error_code = "REQUEST__RECEIVE_ERROR"
    message = "already received request"


class AlreadyFriends(CustomException):
    code = 409
    error_code = "REQUEST__FRIENDS_ERROR"
    message = "already friends"
