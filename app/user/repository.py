from datetime import datetime
from typing import Optional

from loguru import logger
from pydantic import UUID4
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from core import exceptions
from core.utils import password_helper


class UserRepository:
    @classmethod
    async def find_all(cls, session: AsyncSession) -> list[models.User]:
        """
        Retrieve all users from the database.

        Returns:
            list[models.User]: A list of all users in the database.
        """
        users = (await session.execute(select(models.User))).scalars().all()
        return users

    @classmethod
    async def find_by_id(cls, session: AsyncSession, user_id: UUID4) -> Optional[models.User]:
        """
        Retrieve a user by their UUID.

        Args:
            user_id (UUID4): The unique identifier of the user.
            session (AsyncSession): The database session.

        Returns:
            Optional[models.User]: The user with the specified UUID.

        """
        user = (await session.execute(
            select(
                models.User
            ).filter(
                models.User.id_ == user_id
            )
        )).scalars().first()

        return user

    @classmethod
    async def find_by_username(cls, session: AsyncSession, username: str) -> Optional[models.User]:
        """
        Retrieve a user by their username.

        Args:
            session (AsyncSession): The database session.
            username (str): The username of the user.

        Returns:
            Optional[models.User]: The user with the specified username.

        """
        user = (await session.execute(select(models.User).filter(models.User.username == username))).scalars().first()

        return user

    @classmethod
    async def find_by_email(cls, session: AsyncSession, email: str) -> Optional[models.User]:
        """
        Retrieve a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            Optional[models.User]: The user with the specified email.

        """
        user = (await session.execute(select(models.User).filter(models.User.email == email))).scalars().first()

        return user

    @classmethod
    async def add(cls, session: AsyncSession, user: models.User) -> models.User:
        """
        Create a new user in the database.

        Args:
            session (AsyncSession): The database session.
            user (auth_schemas.UserCreate): User creation data.

        Returns:
            models.User: The newly created user.

        Raises:
            HTTPException: if there's an error during the creation process.
        """
        try:
            session.add(user)
            await session.commit()
            return user
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
                logger.error(msg)
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
                logger.error(msg)

            await session.rollback()
            raise exceptions.base.DatabaseException()

    @classmethod
    async def update(cls, session: AsyncSession, user: models.User):
        """
        Update the verification status of a user to True.

        Args:
            session (AsyncSession): The database session.
            user (models.User): The user whose verification status needs to be updated.

        Returns:
            models.User: The updated user object with the verification status set to True.

        Raises:
            HTTPException: If there is an error updating the verification status in the database.
        """
        try:
            session.add(user)
            await session.commit()
            return user
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
                logger.error(msg)
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
                logger.error(msg)

            await session.rollback()
            raise exceptions.base.DatabaseException()

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: UUID4):
        """
        Delete a user from the database.

        Args:
            session (AsyncSession): The database session.
            user_id (UUID4): The unique identifier of the user to delete.

        Raises:
            HTTPException: If there is an error deleting the user from the database.
        """
        try:
            await session.execute(delete(models.User).where(models.User.id_ == user_id))
            await session.commit()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
                logger.error(msg)
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
                logger.error(msg)

            await session.rollback()
            raise exceptions.base.DatabaseException()
