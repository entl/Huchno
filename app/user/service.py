from typing import Optional

from pydantic import UUID4

from app.user.repository import UserRepository
from app.user.schemas import UserOut, UserCreate, UserUpdate, LoginResponse
from app.user.models import User
from core import exceptions

from core.db.session import async_session_factory
from core.utils import password_helper
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def get_all_users(self) -> list[UserOut]:
        async with async_session_factory() as session:
            users = await self.user_repository.find_all(session=session)
            return [UserOut.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: UUID4) -> Optional[UserOut]:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_id(session=session, user_id=user_id)
            return UserOut.model_validate(user) if user else None

    async def get_user_by_username(self, username: str) -> Optional[UserOut]:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_username(session=session, username=username)
            return UserOut.model_validate(user) if user else None

    async def get_user_by_email(self, email: str) -> Optional[UserOut]:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_email(session=session, email=email)
            return UserOut.model_validate(user) if user else None

    async def create_user(self, user: UserCreate) -> UserOut:
        if await self.get_user_by_username(user.username):
            raise exceptions.user.DuplicateEmailOrNicknameException()
        if await self.get_user_by_email(user.email):
            raise exceptions.user.DuplicateEmailOrNicknameException()

        # hash the password
        hashed_password = password_helper.hash(user.password)
        user.password = hashed_password

        async with async_session_factory() as session:
            user: User = User(**user.model_dump())
            user = await self.user_repository.add(session=session, user=user)
            return UserOut.model_validate(user)

    async def update_user(self, user: UserUpdate) -> UserOut:
        if not await self.get_user_by_id(user.id):
            raise exceptions.user.UserNotFoundException()
        async with async_session_factory() as session:
            new_values = user.model_dump(exclude_none=True, exclude_unset=True)
            user_model = await self.user_repository.update(session=session, new_values=new_values, user_id=user.id)
            return UserOut.model_validate(user_model)

    async def delete_user(self, user_id: str) -> None:
        if not await self.get_user_by_id(user_id):
            raise exceptions.user.UserNotFoundException()
        async with async_session_factory() as session:
            await self.user_repository.delete(session=session, user_id=user_id)

    async def login(self, email: str, password: str) -> LoginResponse:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_email(session=session, email=email)
        if not user:
            raise exceptions.user.UserNotFoundException()
        if not password_helper.verify(password, user.password):
            raise exceptions.user.PasswordDoesNotMatchException()

        response = LoginResponse(
            access_token=TokenHelper.encode(payload={"user_id": str(user.id)}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
            token_type="bearer"
        )

        return response

    async def is_admin(self, user_id: str) -> bool:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_id(session=session, user_id=user_id)
        if not user:
            raise exceptions.user.UserNotFoundException()
        return user.is_admin

    async def logout(self):
        raise NotImplementedError
