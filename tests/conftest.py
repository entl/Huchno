import asyncio
from typing import Generator

import alembic
import pytest
from alembic import command
from alembic.config import Config
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (async_sessionmaker, AsyncSession,
                                    create_async_engine, AsyncEngine)

from core.config import settings

from core.utils.token_helper import TokenHelper
from main import app

fake = Faker()

# Defining database for testing
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.pg_database_username}:{settings.pg_database_password}" \
                          f"@{settings.pg_database_hostname}:{settings.pg_database_port}/{settings.pg_database_name}"

async_testing_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
async_testing_session = async_sessionmaker(autoflush=False,
                                           autocommit=False,
                                           bind=async_testing_engine,
                                           expire_on_commit=False)


# @pytest.fixture()
# async def prepare_databases() -> None:
#     # first drop database from previous testing
#     async with async_testing_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
#     # create table after drop to have possibility check in pgadmin
#     async with async_testing_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session")
def alembic_config():
    # Load Alembic configuration
    alembic_cfg = Config("alembic.ini")  # Replace with your Alembic config path
    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(alembic_config):
    # Perform migrations before tests start
    command.upgrade(alembic_config, "head")
    yield
    # Clean up after tests are done
    command.downgrade(alembic_config, "base")


@pytest.fixture()
async def session() -> Generator[AsyncSession, None, None]:
    db = async_testing_session()
    try:
        yield db
    finally:
        await db.close()


# setup
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def async_client(session: AsyncSession) -> AsyncClient:
    # overrides dependency in the routes
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


class UserFactory:
    def __init__(self, async_client: AsyncClient, session: AsyncSession) -> None:
        self.async_client = async_client
        self.session = session

    async def create_user(self, user_data: dict) -> dict:
        res = await self.async_client.post("/users/", json=user_data)
        assert res.status_code == 201
        new_user = res.json()
        new_user["email"] = user_data["email"]
        new_user["password"] = user_data["password"]
        return new_user

    def authorize_client(self, user_id: str) -> AsyncClient:
        token = TokenHelper.encode(payload={"user_id": user_id})
        return self._set_authorization_header(token)

    def _set_authorization_header(self, token: str) -> AsyncClient:
        self.async_client.headers.update({"Authorization": f"Bearer {token}"})
        return self.async_client
