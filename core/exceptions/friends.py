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


class SameUser(CustomException):
    code = 409
    error_code = "REQUEST__SAME_USER_ERROR"
    message = "same user"


class FriendshipNotFound(CustomException):
    code = 404
    error_code = "FRIENDSHIP_NOT_FOUND"
    message = "friendship not found"


class UsersNotFriends(CustomException):
    code = 409
    error_code = "USERS__NOT_FRIENDS_ERROR"
    message = "users are not friends"
