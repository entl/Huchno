from datetime import datetime

from pydantic import BaseModel, Field, UUID4


class MessageBase(BaseModel):
    """
    Base model for a message without unique identifiers.

    Attributes:
        recipient_id (UUID4): The UUID of the message's recipient.
        content (str): The content of the message.
    """
    recipient_id: UUID4
    content: str


class MessageIn(MessageBase):
    """
    Model for incoming messages.

    Attributes:
        sender_id (UUID4): The UUID of the message's sender.
    """
    sender_id: UUID4


class MessageOut(MessageIn):
    """
    Model for outgoing messages, including their MongoDB identifier.

    Attributes:
        id (ObjectIdField): The MongoDB Object ID of the message.
        sender_id (UUID4): The UUID of the message's sender.
        date_created (datetime): The date and time when the message was created.
    """
    # alias for Mongo id
    id: UUID4 = Field(alias="_id")
    created_at: datetime

    class Config:
        """
        Configuration for the message model.

        Attributes:
            allow_population_by_field_name (bool): Enable populating model fields using field names as well as aliases.
        """
        # allows to populate model with field names instead of aliases
        populate_by_name = True
