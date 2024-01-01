from typing import AsyncIterable

from pydantic import UUID4

from app.chat.models import Message
from app.chat.repository import MessageRepository
from app.chat.schemas import MessageOut, MessageIn
from core.db.mongo_session import get_message_collection


class MessageService:
    def __init__(self):
        self.message_repository = MessageRepository()

    async def get_messages(self, sender_id: UUID4, recipient_id: UUID4) -> list[MessageOut]:
        res = await self.message_repository.find_by_sender_id_recipient_id(
            sender_id=sender_id,
            recipient_id=recipient_id,
        )

        return [MessageOut.model_validate(message.__dict__) for message in res]

    async def send_message(self, message: MessageIn) -> MessageOut:
        res = await self.message_repository.add(message=Message.model_validate(message.model_dump()))

        return MessageOut.model_validate(res.__dict__)

    async def subscribe_to_change_stream(self, user_id: UUID4) -> AsyncIterable[MessageOut]:
        collection = await get_message_collection()

        async with collection.watch() as stream:
            async for change in stream:
                if change["fullDocument"]["recipient_id"] == user_id:
                    yield MessageOut.model_validate(change["fullDocument"])
