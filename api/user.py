from typing import Annotated

from loguru import logger
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import UUID4

from app.user.schemas import UserCreate, UserOut, UserUpdate
from app.user.service import UserService

from core import exceptions

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=list[UserOut], status_code=status.HTTP_200_OK)
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


@users_router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: UUID4, user_service: Annotated[UserService, Depends()]):
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


@users_router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED,)
async def create_user(user_service: Annotated[UserService, Depends()], user: UserCreate):
    """
    Create a new user.

    Args:
        user_service (UserService): User Service instance.
        user (UserCreate): User data to create.

    Returns:
        UserOut: Created user data.
    """
    return await user_service.create_user(user=user)


@users_router.patch("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(user_service: Annotated[UserService, Depends()], user: UserUpdate, user_id: UUID4):
    """
    Update a user.

    Args:
        user_service (UserService): User Service instance.
        user (UserUpdate): User data to update.
        user_id (str): The ID of the user to update.

    Returns:
        UserOut: Updated user data.
    """
    return await user_service.update_user(user)


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_service: Annotated[UserService, Depends()], user_id: UUID4):
    """
    Delete a user.

    Args:
        user_service (UserService): User Service instance.
        user_id (str): The ID of the user to delete.

    Returns:
        None
    """
    await user_service.delete_user(user_id=user_id)
