from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4

from app.friends.service import FriendshipService
from core.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated, IsAdmin
from core.fastapi.schemas.current_user import CurrentUser
from app.friends.schemas import FriendshipRequestIn

friends_router = APIRouter(prefix="/friends", tags=["Friends"])


@friends_router.get("/")
async def get_all_friends(
        friendship_service: Annotated[FriendshipService, Depends()],
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )]
):
    return await friendship_service.get_friends(user_id=str(current_user.id))


@friends_router.get("/requests/sent")
async def get_sent_friendship_requests(
        friendship_service: Annotated[FriendshipService, Depends()],
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )]
):
    return await friendship_service.get_sent_friendship_requests(user_id=str(current_user.id))


@friends_router.get("/requests/received")
async def get_received_friendship_requests(
        friendship_service: Annotated[FriendshipService, Depends()],
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )]
):
    return await friendship_service.get_received_friendship_requests(user_id=str(current_user.id))


@friends_router.post("/")
async def send_friend_request(
        request: FriendshipRequestIn,
        friendship_service: Annotated[FriendshipService, Depends()],
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )]
):
    request = await friendship_service.send_friend_request(
        user_id=str(current_user.id),
        friend_id=str(request.addressee_id)
    )
    return request


@friends_router.patch("/{friendship_id}/accept")
async def accept_friend_request(
        friendship_id: UUID4,
        friendship_service: Annotated[FriendshipService, Depends()],
        current_user: Annotated[CurrentUser, Depends(
            PermissionDependency([IsAuthenticated], all_required=True)
        )]
):
    friendship = await friendship_service.accept_friendship_request(
        friendship_id=friendship_id
    )
    return friendship


@friends_router.patch("/{friendship_id}/decline")
async def decline_friend_request():
    pass


@friends_router.delete("/{friendship_id}")
async def delete_friendship():
    pass
