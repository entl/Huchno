from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field

from core.config import settings


class Message(Document):
    id: UUID = Field(default_factory=uuid4)
    recipient_id: UUID = Field(...)
    sender_id: UUID = Field(...)
    content: str
    created_at: Annotated[datetime, Field(default=datetime.now(), Literal=True)]

    class Settings:
        collection = settings.mongo_messages_collection_name
