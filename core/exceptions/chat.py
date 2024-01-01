from core.exceptions.base import CustomException


class MessageToSelfException(CustomException):
    code = 400
    error_code = "MESSAGE_TO_SELF"
    message = "cannot send message to self"


class MessageToNonFriendException(CustomException):
    code = 400
    error_code = "MESSAGE_TO_NON_FRIEND"
    message = "cannot send message to non friend"

