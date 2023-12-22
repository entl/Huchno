from typing import Tuple

from pydantic import UUID4
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.fastapi.schemas.current_user import CurrentUser
from core.exceptions.token import TokenException
from core.utils.token_helper import TokenHelper


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, UUID4]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            token_type, payload_encoded = authorization.split(" ")
            if token_type.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not payload_encoded:
            return False, current_user

        try:
            payload = TokenHelper.decode(payload_encoded)
            user_id = payload.get("user_id")
        except TokenException:
            return False, current_user

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
