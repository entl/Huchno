from abc import ABC
from contextvars import ContextVar

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, async_scoped_session, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from core.config import settings

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.pg_database_username}:{settings.pg_database_password}" \
                          f"@{settings.pg_database_hostname}/{settings.pg_database_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
async_session_factory = async_sessionmaker(autoflush=False, autocommit=False, bind=engine, expire_on_commit=False)

Base = declarative_base()


class UnitOfWorkBase(ABC):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    async def commit(self):
        raise NotImplementedError()

    async def rollback(self):
        raise NotImplementedError()

    async def close(self):
        raise NotImplementedError()

    async def refresh(self, entity):
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print("Rolling back transaction")
            await self.session.rollback()
        else:
            print("Committing transaction")
            await self.session.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()

    async def refresh(self, entity: DeclarativeBase):
        await self.session.refresh(entity)
