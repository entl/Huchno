from .base import (
    CustomException,
    BadRequestException,
    NotFoundException,
    ForbiddenException,
    UnprocessableEntity,
    DuplicateValueException,
    UnauthorizedException,
)
from .token import DecodeTokenException, ExpiredTokenException, TokenException
from .user import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
    UserNotVerified,
    InsufficientPermissions,
    UserAgeInvalid
)
from .friends import (
    AlreadySentRequest,
    AlreadyReceivedRequest,
    AlreadyFriends
)

from .chat import (
    MessageToSelfException,
    MessageToNonFriendException
)

__all__ = [
    "CustomException",
    "BadRequestException",
    "NotFoundException",
    "ForbiddenException",
    "UnprocessableEntity",
    "DuplicateValueException",
    "UnauthorizedException",
    "DecodeTokenException",
    "ExpiredTokenException",
    "PasswordDoesNotMatchException",
    "DuplicateEmailOrNicknameException",
    "UserNotFoundException",
    "UserNotVerified",
    "AlreadySentRequest",
    "AlreadyReceivedRequest",
    "AlreadyFriends",
    "InsufficientPermissions",
    "UserAgeInvalid",
    "TokenException",
    "MessageToSelfException",
    "MessageToNonFriendException"
]
