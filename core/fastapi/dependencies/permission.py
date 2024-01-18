from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request, WebSocket, WebSocketException
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from loguru import logger
from starlette import status

from app.user.service import UserService
from core.exceptions import CustomException, UnauthorizedException
from core.fastapi.schemas.current_user import CurrentUser


class Permissions:
    IsAuthenticated = "IsAuthenticated"
    IsAdmin = "IsAdmin"
    AllowAll = "AllowAll"


class BasePermission(ABC):
    exception = CustomException
    alias: str = None

    @abstractmethod
    async def has_permission(self, request: Request | WebSocket) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException
    alias = Permissions.IsAuthenticated

    async def has_permission(self, request: Request | WebSocket) -> bool:
        return request.user.id is not None


class AllowAll(BasePermission):
    alias = Permissions.AllowAll

    async def has_permission(self, request: Request | WebSocket) -> bool:
        return True


class IsAdmin(BasePermission):
    exception = UnauthorizedException
    alias = Permissions.IsAdmin

    async def has_permission(self, request: Request | WebSocket) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await UserService().is_admin(user_id=user_id)


class PermissionDependencyBase(SecurityBase, ABC):
    @abstractmethod
    async def __call__(self, request: Request | WebSocket) -> CurrentUser:
        pass

    @abstractmethod
    async def is_user_has_all_permissions(self, request: Request | WebSocket) -> List[str]:
        pass

    @abstractmethod
    async def is_user_has_any_permissions(self, request: Request | WebSocket) -> List[str]:
        pass


class PermissionDependencyHTTP(PermissionDependencyBase):
    def __init__(self, permissions: List[Type[BasePermission]], all_required: bool = True):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__
        self.all_required = all_required

    async def __call__(self, request: Request):
        if not self.all_required:
            allowed_permissions = await self.is_user_has_any_permissions(request=request)
            return CurrentUser(id=request.user.id, permissions=allowed_permissions)
        if self.all_required:
            allowed_permissions = await self.is_user_has_all_permissions(request=request)
            return CurrentUser(id=request.user.id, permissions=allowed_permissions)

    async def is_user_has_any_permissions(self, request: Request) -> List[str]:
        allowed_permissions = []

        for permission in self.permissions:
            cls = permission()
            if await cls.has_permission(request=request):
                allowed_permissions.append(cls.alias)

        if allowed_permissions:
            return allowed_permissions

        raise UnauthorizedException

    async def is_user_has_all_permissions(self, request: Request) -> List[str]:
        allowed_permissions = []

        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception
            allowed_permissions.append(cls.alias)

        return allowed_permissions


class PermissionDependencyWebsocket(PermissionDependencyBase):
    def __init__(self, permissions: List[Type[BasePermission]], all_required: bool = True):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__
        self.all_required = all_required

    async def __call__(self, websocket: WebSocket):
        if not self.all_required:
            allowed_permissions = await self.is_user_has_any_permissions(websocket=websocket)
            return CurrentUser(id=websocket.user.id, permissions=allowed_permissions)
        if self.all_required:
            allowed_permissions = await self.is_user_has_all_permissions(websocket=websocket)
            return CurrentUser(id=websocket.user.id, permissions=allowed_permissions)

    async def is_user_has_any_permissions(self, websocket: WebSocket) -> List[str]:
        allowed_permissions = []

        for permission in self.permissions:
            cls = permission()
            if await cls.has_permission(request=websocket):
                allowed_permissions.append(cls.alias)

        if allowed_permissions:
            return allowed_permissions

        raise UnauthorizedException

    async def is_user_has_all_permissions(self, websocket: WebSocket) -> List[str]:
        allowed_permissions = []

        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=websocket):
                raise cls.exception
            allowed_permissions.append(cls.alias)

        return allowed_permissions
