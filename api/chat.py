import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pydantic import UUID4
from sse_starlette import EventSourceResponse

from app.chat.service import MessageService
from app.chat.schemas import MessageIn, MessageBase
from app.friends.service import FriendshipService
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.fastapi.schemas.current_user import CurrentUser
from core.exceptions import MessageToSelfException, MessageToNonFriendException

chat_router = APIRouter(prefix="/chats", tags=["Chats"])

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond


def is_message_to_self(sender_id: UUID4, recipient_id: UUID4) -> bool:
    return sender_id == recipient_id


@chat_router.post("/")
async def send_message(
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )],
        message_service: Annotated[MessageService, Depends()],
        friendship_service: Annotated[FriendshipService, Depends()],
        message: MessageBase
):
    if is_message_to_self(sender_id=current_user.id, recipient_id=message.recipient_id):
        raise MessageToSelfException()

    # if not await friendship_service.is_users_friends(user_id=current_user.id, friend_id=message.recipient_id):
    #     raise MessageToNonFriendException()

    return await message_service.send_message(
        message=MessageIn.model_validate({**message.model_dump(), "sender_id": current_user.id})
    )


@chat_router.get("/stream")
async def message_stream(
        message_service: Annotated[MessageService, Depends()],
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )],
):
    async def casting():
        async for change in message_service.subscribe_to_change_stream(user_id=current_user.id):
            if change:
                yield {
                    "event": "new_message",
                    "id": change.id,
                    "data": change.model_dump_json()
                }

    return EventSourceResponse(casting(), media_type="text/event-stream")


@chat_router.get("/{recipient_id}")
async def get_messages(
        recipient_id: UUID4,
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )],
        message_service: Annotated[MessageService, Depends()],
):
    return await message_service.get_messages(sender_id=current_user.id, recipient_id=recipient_id)
