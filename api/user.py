from typing import Annotated

from loguru import logger
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.user.schemas import UserCreate, UserOut
from app.user.service import UserService

from core import exceptions

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=list[UserOut])
async def get_all_users(user_service: Annotated[UserService, Depends()]):
    """
    Get all users.

    This endpoint retrieves all users from the database.

    Args:
        user_service (UserService): User Service instance.

    Returns:
        list[UserOut]: A list of all users in the database.
    """
    users = await user_service.get_all_users()
    return users


@users_router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: str, user_service: Annotated[UserService, Depends()]):
    """
    Get user by ID.

    This endpoint retrieves a user from the database by their ID.

    Args:
        user_id (str): The ID of the user.
        user_service (UserService): User Service instance.

    Returns:
        UserOut: The user with the specified ID.
    """
    user = await user_service.get_user_by_id(user_id=user_id)
    if not user:
        raise exceptions.user.UserNotFoundException()

    return user


@users_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user_service: Annotated[UserService, Depends()], user: UserCreate):
    user: UserOut = await user_service.create_user(user=user)
    return user
