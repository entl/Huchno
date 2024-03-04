from datetime import datetime, date, timedelta
from typing import Optional, Annotated

from pydantic import EmailStr, Field, field_validator, BaseModel, UUID4, validator, HttpUrl

from core import exceptions
from core.config import settings


class ProfileImageIn(BaseModel):
    """
    Represents the input model for a user's profile image.

    Attributes:
        filename (str): The filename of the profile image. Default is the default profile image filename.

    """
    filename: str = Field(default=settings.default_profile_image)

    # when user hasn't uploaded file, it may send with value of null
    # however pydantic considers it as a string, so default value isn't set
    @field_validator('filename')
    def validate_filename(cls, value):
        if value == 'null' or value == '':
            return 'default.jpg'
        return value


class ProfileImageOut(ProfileImageIn):
    """
    Represents the output model for a user's profile image.

    Attributes:
        url (HttpUrl): The URL of the profile image.

    """
    url: HttpUrl


class UserBase(BaseModel):
    """
    Represents the base model for user information.

    Attributes:
        username (str): The username of the user.
        fullname (str): The full name of the user.
        birthdate (date): The birthdate of the user.
        is_active (bool): The user's active status.
        last_login (datetime): The datetime of the user's last login.

    """
    username: Annotated[str, Field(pattern="^[A-Za-z0-9-_.]+$", to_lower=True,
                                   strip_whitespace=True, description="The username of the user",
                                   min_length=4, max_length=128)]
    fullname: Annotated[str, Field(min_length=1, max_length=128, description="The full name of the user")]
    birthdate: Annotated[date, Field(..., description="The birthdate of the user")]
    is_active: Annotated[bool, Field(default=False, description="The user's active status")]
    last_login: Annotated[datetime | None, Field(default=None, description="The datetime of the user's last login")]

    # restricts age bigger than 100 and lower than 14
    @field_validator('birthdate')
    def validate_birthdate(cls, value):
        today = date.today()
        min_date = today - timedelta(days=100 * 365)
        max_date = today - timedelta(days=14 * 365)
        if value < min_date or value > max_date:
            raise exceptions.user.UserAgeInvalid(f'birthdate must be between {min_date} and {max_date}')
        return value


class UserCreate(UserBase):
    """
    Represents the input model for creating a new user.

    Attributes:
        email (EmailStr): The email of the user.
        password (str): The password of the user.
        verified (bool): The verification status of the user.
    """
    email: Annotated[EmailStr, Field(..., description="The email of the user")]
    password: Annotated[str, Field(..., min_length=8, max_length=128)]
    verified: Annotated[bool, Field(default=False, Literal=True)]
    profile_image: ProfileImageIn


class UserOut(UserBase):
    """
    Represents the output model for user information.

    Attributes:
        id (UUID4): The unique identifier of the user.
        registration_date (datetime): The registration datetime of the user.
        profile_image (ProfileImageOut): The profile image of the user.

    """
    id: Annotated[UUID4, Field(..., description="The unique identifier of the user")]
    registration_date: Annotated[date, Field(..., description="The registration datetime of the user")]
    email: Annotated[EmailStr, Field(..., description="The email of the user")]
    profile_image: ProfileImageOut
    verified: Annotated[bool, Field(..., description="The verification status of the user")]

    class Config:
        from_attributes = True
        populate_by_name = True


class UserUpdate(BaseModel):
    id: Annotated[UUID4, Field(..., description="The unique identifier of the user")]
    email: Optional[EmailStr] = Field(default=None, description="The email of the user")
    username: Optional[str] = Field(default=None, pattern="^[A-Za-z0-9-_.]+$", to_lower=True, strip_whitespace=True,
                                    description="The username of the user", min_length=4, max_length=128)
    fullname: Optional[str] = Field(default=None, min_length=1, max_length=128, description="The full name of the user")
    birthdate: Optional[date] = Field(default=None, description="The birthdate of the user")
    profile_image: Optional[ProfileImageOut] = Field(default=None, description="The profile image of the user")
    is_active: Optional[bool] = Field(default=None, description="The user's active status")
    registration_date: Optional[date] = Field(default=None, description="The registration datetime of the user")
    last_login: Optional[datetime] = Field(default=None, description="The datetime of the user's last login")
    verified: Optional[bool] = Field(default=None, description="The verification status of the user")

    # restricts age bigger than 100 and lower than 14
    @field_validator('birthdate')
    def validate_birthdate(cls, value):
        today = date.today()
        min_date = today - timedelta(days=100 * 365)
        max_date = today - timedelta(days=14 * 365)
        if value < min_date or value > max_date:
            raise exceptions.user.UserAgeInvalid(f'birthdate must be between {min_date} and {max_date}')
        return value


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field(..., description="Type of token")
