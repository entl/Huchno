import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, DATE

from core.db.session import Base
from core.config import settings


class User(Base):
    """
        A model representing a user in the application.

        Attributes:
            id_ (UUID): The unique identifier for the user.
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The hashed password of the user.
            fullname (str): The full name of the user.
            birthdate (datetime): The birthdate of the user.
            profile_image (str): The profile image URL of the user.
            registration_date (datetime): The date and time of user registration.
            is_active (bool): Indicates if the user is active.
            last_login (datetime): The date and time of the user's last login.
            spotify_data (UserSpotifyData): Associated Spotify data for the user.
    """
    __tablename__ = 'users'

    id_ = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    birthdate = Column(DATE(), nullable=False)
    profile_image = Column(String, server_default=settings.default_profile_image, nullable=False)
    registration_date = Column(DATE(), server_default=func.current_date(), nullable=False)
    is_active = Column(Boolean, server_default="False", nullable=True)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    verified = Column(Boolean, server_default="False", nullable=False)
    is_admin = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now())
    #
    # spotify_data = relationship("UserSpotifyData", back_populates="user",
    #                             lazy="selectin", uselist=False)
    #
    # def friends(self):
    #     return select(Friendship, User) \
    #         .join(User, Friendship.addressee_id == User.id_) \
    #         .filter(and_(Friendship.requester_id == self.id_, Friendship.status == "accepted"))
    #
    # def sent_requests(self):
    #     return select(Friendship, User) \
    #         .join(User, Friendship.addressee_id == User.id_) \
    #         .filter(and_(Friendship.requester_id == self.id_, Friendship.status == "sent"))
    #
    # def received_requests(self):
    #     return select(Friendship, User) \
    #         .join(User, Friendship.addressee_id == User.id_) \
    #         .filter(and_(Friendship.requester_id == self.id_, Friendship.status == "pending"))