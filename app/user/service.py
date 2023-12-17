from pydantic import UUID4

from app.user.repository import UserRepository
from app.user.schemas import UserOut, UserCreate
from app.user.models import User
from core import exceptions

from core.db.session import async_session_factory
from core.utils import password_helper


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def get_all_users(self) -> list[UserOut]:
        async with async_session_factory() as session:
            users = await self.user_repository.find_all(session=session)
            return [UserOut.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: UUID4) -> UserOut:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_id(session=session, user_id=user_id)
            return UserOut.model_validate(user)

    async def get_user_by_username(self, username: str) -> UserOut:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_username(session=session, username=username)
            return UserOut.model_validate(user)

    async def get_user_by_email(self, email: str) -> UserOut:
        async with async_session_factory() as session:
            user = await self.user_repository.find_by_email(session=session, email=email)
            return UserOut.model_validate(user)

    async def create_user(self, user: UserCreate) -> UserOut:
        if self.get_user_by_username(user.username):
            raise exceptions.user.DuplicateEmailOrNicknameException()
        if self.get_user_by_email(user.email):
            raise exceptions.user.DuplicateEmailOrNicknameException()

        # hash the password
        hashed_password = password_helper.hash(user.password)
        user.password = hashed_password

        async with async_session_factory() as session:
            user: User = User(**user.model_dump())
            user = await self.user_repository.add(session=session, user=user)
            return UserOut.model_validate(user)

    async def update_user(self):
        raise NotImplementedError

    async def delete_user(self):
        raise NotImplementedError

    async def login(self):
        raise NotImplementedError

    async def logout(self):
        raise NotImplementedError
