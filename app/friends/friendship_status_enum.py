import enum


class FriendshipStatusEnum(enum.Enum):
    sent = 'sent'
    pending = 'pending'
    declined = 'declined'
    accepted = 'accepted'
    blocked = 'blocked'
