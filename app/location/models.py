from sqlalchemy import Column, ForeignKey, Double
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from core.db.session import Base


class Location(Base):
    __tablename__ = 'location'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    latitude = Column(Double(), nullable=False)
    longitude = Column(Double(), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now())
