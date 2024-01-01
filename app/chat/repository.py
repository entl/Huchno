from typing import List

from pydantic import UUID4

from . import schemas
from .models import Message


class MessageRepository:
    model = Message

    @classmethod
    async def find_by_id(cls, message_id: str) -> Message:
        """
        Retrieve a message from the messages' collection.

        Args:
            message_id (UUID4): ID of the message.

        Returns:
            Dict: Dictionary containing the message data.
        """

        return await cls.model.find_one({'_id': message_id})

    @classmethod
    async def find_by_sender_id_recipient_id(cls, sender_id: UUID4, recipient_id: UUID4) -> list[Message]:
        """
        Retrieve messages between sender and recipient from the messages' collection.

        Args:
            sender_id (UUID4): ID of the sender user.
            recipient_id (UUID4): ID of the recipient user.

        Returns:
            List[Dict]: List of message dictionaries.
        """

        messages = await cls.model.find(
            Message.sender_id == sender_id,
            Message.recipient_id == recipient_id
        ).to_list()

        return messages

    @classmethod
    async def add(cls, message: Message) -> Message:
        """
        Create a new message and insert it into the messages' collection.

        Args:
            message (schemas.MessageIn): Message input data.
        """

        new_message = await cls.model.insert_one(message)
        return new_message
