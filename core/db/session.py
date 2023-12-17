from contextvars import ContextVar

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, async_scoped_session
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

