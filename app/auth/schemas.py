from pydantic import BaseModel, Field


class RefreshTokenBase(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field(..., description="Token type")


class RefreshTokenRequest(RefreshTokenBase):
    pass


class RefreshTokenResponse(RefreshTokenBase):
    pass


class VerifyTokenRequest(BaseModel):
    token: str = Field(..., description="Token")