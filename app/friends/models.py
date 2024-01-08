import uuid

from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.friends.friendship_status_enum import FriendshipStatusEnum
from core.db.session import Base


class Friendship(Base):
    """
        A model representing the friendship status between users.

        Attributes:
            id_ (UUID): The unique identifier for the friendship.
            requester_id (UUID): The user who initiated the friendship request.
            addressee_id (UUID): The user who received the friendship request.
            status (StatusEnum): The status of the friendship request.
            request_date (datetime): The date and time when the request was made.
            accept_date (datetime): The date and time when the request was accepted.
    """
    __tablename__ = 'friendships'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    requester_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    addressee_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    status = Column(Enum(FriendshipStatusEnum), nullable=False)
    request_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    accept_date = Column(TIMESTAMP(timezone=True), server_default=None, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now())

    requester = relationship("User", foreign_keys=[requester_id], lazy="selectin")
    addressee = relationship("User", foreign_keys=[addressee_id], lazy="selectin")

    # def requester(self):
    #     # import here to avoid circular import
    #     from app.user.models import User
    #     """Query the user who initiated the friendship request."""
    #     return select(User) \
    #         .filter(User.id_ == self.requester_id)
    #
    # def addressee(self):
    #     # import here to avoid circular import
    #     from app.user.models import User
    #     """Query the user who received the friendship request."""
    #     return select(User) \
    #         .filter(User.id_ == self.addressee_id)
