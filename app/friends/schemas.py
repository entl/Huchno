from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, UUID4

from app.friends.friendship_status_enum import FriendshipStatusEnum
from app.user.schemas import UserOut


class BaseFriendshipRequest(BaseModel):
    addressee_id: UUID4 = Field(alias="friend_id")
    status: Enum | str

    class Config:
        from_attributes = True
        # allows to populate model with field names instead of aliases
        populate_by_name = True


class FriendshipRequestIn(BaseFriendshipRequest):
    status: str = Field(default=FriendshipStatusEnum.sent.value, Literal=True)


class FriendshipOut(BaseFriendshipRequest):
    id: UUID4 = Field(alias="id")
    user: UserOut = Field(..., description="User details of the second user")
    accept_date: datetime | None = Field(None, description="The date when the friendship was accepted")
    request_date: datetime = Field(None, description="The date when the friendship was requested")


