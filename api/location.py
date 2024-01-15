from typing import Annotated

from fastapi import APIRouter, Depends, status, WebSocket
from fastapi.websockets import WebSocketDisconnect
from pydantic import UUID4
from sse_starlette import EventSourceResponse

from app.friends.service import FriendshipService

from app.location.schemas import LocationBase, LocationOut
from app.location.service import LocationService

from core.exceptions import UsersNotFriends
from core.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated, IsAdmin
from core.fastapi.schemas.current_user import CurrentUser

location_router = APIRouter(prefix="/location", tags=["Location"])


@location_router.get(
    "/{user_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
)
async def get_user_location(
    user_id: UUID4,
    current_user: Annotated[CurrentUser, Depends(
        PermissionDependency([IsAuthenticated, IsAdmin], all_required=False)
    )],
    location_service: Annotated[LocationService, Depends()]
):
    if not await FriendshipService().is_users_friends(user_id=current_user.id, friend_id=user_id):
        raise UsersNotFriends()

    location = await location_service.get_location_by_user_id(user_id=user_id)

    return location


@location_router.post(
    "/",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
)
async def set_user_location(
        location: LocationBase,
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=False)
        )],
        location_service: Annotated[LocationService, Depends()]
):
    return await location_service.set_or_update_location_by_user_id(location=location, user_id=current_user.id)


@location_router.websocket("/ws")
async def publish_live_location(
        websocket: WebSocket,
        location_service: Annotated[LocationService, Depends()],
):
    await websocket.accept()
    # TODO: authentication
    try:
        while True:
            location = await websocket.receive_json()
            location_serialised = LocationBase(**location)
            await location_service.publish_location(location=location_serialised, user_id="c44f065b-b30d-48a5-8d76-2786271b3832")
    except WebSocketDisconnect as e:
        pass


@location_router.get("/stream/{user_id}")
async def message_stream(
        location_service: Annotated[LocationService, Depends()],
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )],
        user_id: UUID4
):
    async def casting():
        async for change in location_service.subscribe_location_with_user_id(user_id=str(user_id)):
            if change:
                yield {
                    "event": "new_message",
                    "data": change
                }

    return EventSourceResponse(casting(), media_type="text/event-stream")