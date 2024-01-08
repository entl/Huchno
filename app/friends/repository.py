from datetime import datetime
from typing import Optional, Sequence, Tuple

from loguru import logger
from pydantic import UUID4
from sqlalchemy import select, delete, update, and_, or_, Row
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from .friendship_status_enum import FriendshipStatusEnum
from core import exceptions
from .models import Friendship
from app.user.models import User


class FriendsRepository:
    @classmethod
    async def find_all(cls, session: AsyncSession) -> Sequence[Friendship]:
        """
        Retrieve all users from the database.

        Returns:
            list[User]: A list of all users in the database.
        """
        friendships = (await session.execute(select(Friendship))).scalars().all()
        return friendships

    @classmethod
    async def find_by_id(cls, session: AsyncSession, friendship_id: str) -> Optional[Friendship]:
        """
        Retrieve a user by their UUID.

        Args:
            friendship_id (UUID4): The unique identifier of the user.
            session (AsyncSession): The database session.

        Returns:
            Optional[User]: The user with the specified UUID.

        """
        friendship = (await session.execute(
            select(
                Friendship
            ).filter(
                Friendship.id == friendship_id
            )
        )).scalars().first()

        return friendship

    @classmethod
    async def find_by_requester_id_address_id(
            cls,
            session: AsyncSession,
            requester_id: UUID4,
            addressee_id: UUID4
    ) -> Friendship | None:
        """
        Retrieve a friendship request between two users.

        This function queries the database to retrieve a friendship request between a requester and an addressee.
        The function returns `None` if no request exists between the specified users.

        Args:
            requester_id (UUID4): The unique identifier of the user who initiated the request.
            addressee_id (UUID4): The unique identifier of the user who received the request.

        Returns:
            Friendship | None: The retrieved friendship request if it exists, or `None` if not found.
        """
        request = (
            await session.execute(
                select(Friendship).filter(
                    and_(
                        Friendship.requester_id == requester_id,
                        Friendship.addressee_id == addressee_id
                    )
                )
            )
        ).scalars().first()

        return request

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            requester_id: UUID4,
            addressee_id: UUID4
    ) -> tuple[Friendship, Friendship]:
        """
        Create a new friendship requests between two users.

        This function creates new friendship requests by adding adjacency relationships to the database
        for the requester and the addressee. It checks various conditions to ensure the request can be created
        and raises appropriate exceptions if conditions are not met.

        Args:
            requester_id (UUID4): The unique identifier of the user initiating the request.
            addressee_id (UUID4): The unique identifier of the user receiving the request.

        Returns:
            tuple[Friendship, Friendship]: A tuple containing two Friendship models representing
            the send and pending requests.

        Raises:
            HTTPException: Raised if conditions for creating the request are not met or if there is an error
            during the database operation.
        """

        # creating a new adjacency relationships
        request_sent = Friendship(requester_id=requester_id,
                                  addressee_id=addressee_id,
                                  status=FriendshipStatusEnum.sent.value)

        request_pending = Friendship(requester_id=addressee_id,
                                     addressee_id=requester_id,
                                     status=FriendshipStatusEnum.pending.value)

        session.add_all([request_sent, request_pending])
        await session.commit()
        # return tuple of adjacency requests
        return request_sent, request_pending

    @classmethod
    async def find_friends_by_user_id(
            cls,
            session: AsyncSession,
            user_id: str,
            limit: int = None,
            offset: int = None
    ) -> Sequence[Friendship]:
        """
        Retrieve a list of accepted friendship connections for the given user.

        This function queries the database to retrieve a list of friendships where the given user's ID
        appears as the requester and the status is 'accepted'.

        Args:
            limit (int): The maximum number of friends to retrieve.
            offset (int): The number of friends to skip before retrieving.
            user (User): The User model for whom to retrieve friends.

        Returns:
            Sequence[Row[tuple[Friendship, User]]]: A sequence of rows containing tuples where
            the first element is a Friendship model and the second element is a User model representing the friend.
        """
        stmt = select(
            Friendship
        ).filter(
            # when user accepts request 2 requests created with adjacent requester and addressee
            and_(
                Friendship.requester_id == user_id,
                Friendship.status == "accepted"
            )
        )

        return (await session.execute(stmt)).scalars().all()

    @classmethod
    async def find_sent_requests_by_user_id(
            cls,
            session: AsyncSession,
            user_id: str,
            limit: int = None,
            offset: int = None
    ) -> Sequence[Friendship]:
        """
        Retrieve a list of friendship requests sent by the given user.

        This function queries the database to retrieve a list of friendships where the given user's ID
        appears as the requester and the status is 'sent'.

        Args:
            limit (int): The maximum number of requests to retrieve.
            offset (int): The number of requests to skip before retrieving.
            user (User): The User model for whom to retrieve sent friendship requests.

        Returns:
            Sequence[Row[tuple[Friendship, User]]]: A sequence of rows containing tuples where
            the first element is a Friendship model representing the sent request and the second element
            is a User model representing the addressee of the request.
        """
        stmt = select(
            Friendship
        ).filter(
            and_(
                Friendship.requester_id == user_id,
                Friendship.status == "sent"
            )
        )

        return (await session.execute(stmt)).scalars().all()

    @classmethod
    async def find_received_requests_by_user_id(
            cls,
            session: AsyncSession,
            user_id: str,
            limit: int = None,
            offset: int = None
    ) -> Sequence[Friendship]:
        stmt = select(
            Friendship
        ).filter(
            and_(
                Friendship.requester_id == user_id,
                Friendship.status == "pending"
            )
        )

        return (await session.execute(stmt)).scalars().all()

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            friendship_id: str,
            new_values: dict
    ) -> Friendship:
        try:
            query = (
                update(Friendship)
                .where(friendship_id == Friendship.id)
                .values(**new_values)
                .returning(Friendship)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()
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
    async def delete(
            cls,
            session: AsyncSession,
            friendship_id: str
    ) -> None:
        try:
            query = (
                delete(Friendship)
                .where(friendship_id == Friendship.id)
            )
            await session.execute(query)
            await session.commit()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot delete data from table"
                logger.error(msg)
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot delete data from table"
                logger.error(msg)

            await session.rollback()
            raise exceptions.base.DatabaseException()
