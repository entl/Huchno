from typing import Annotated

from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.auth.schemas import RefreshTokenRequest, RefreshTokenResponse, VerifyTokenRequest
from app.auth.jwt_service import JwtService
from app.user.schemas import LoginResponse
from app.user.service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
async def refresh_token(request: RefreshTokenRequest):
    token = await JwtService().create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_token(request: VerifyTokenRequest):
    await JwtService().verify_token(token=request.token)


@auth_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = await UserService().login(email=user_credentials.username, password=user_credentials.password)
    return token
