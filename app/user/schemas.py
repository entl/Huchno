from datetime import datetime, date, timedelta

from pydantic import EmailStr, Field, field_validator, BaseModel, UUID4


class UserBase(BaseModel):
    """
    Represents the base model for user information.

    Attributes:
        username (str): The username of the user.
        fullname (str): The full name of the user.
        birthdate (date): The birthdate of the user.
        profile_image (ProfileImageIn): The profile image of the user.
        is_active (bool): The user's active status.
        last_login (datetime): The datetime of the user's last login.

    """
    username: str = Field(pattern="^[A-Za-z0-9-_.]+$", to_lower=True, strip_whitespace=True)
    fullname: str = Field(min_length=1, max_length=128)
    birthdate: date
    # profile_image: ProfileImageIn
    is_active: bool = False
    last_login: datetime | None = None

    # restricts age bigger than 100 and lower than 14
    @field_validator('birthdate')
    def validate_birthdate(cls, value):
        today = date.today()
        min_date = today - timedelta(days=100 * 365)
        max_date = today - timedelta(days=14 * 365)
        if value < min_date or value > max_date:
            raise ValueError(f'birthdate must be between {min_date} and {max_date}')
        return value


class UserCreate(UserBase):
    """
    Represents the input model for creating a new user.

    Attributes:
        email (EmailStr): The email of the user.
        password (str): The password of the user.

    """
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    verified: bool = Field(default=False, Literal=True)


class UserOut(UserBase):
    """
    Represents the output model for user information.

    Attributes:
        id_ (UUID4): The unique identifier of the user.
        registration_date (datetime): The registration datetime of the user.
        profile_image (ProfileImageOut): The profile image of the user.

    """
    id_: UUID4
    registration_date: date
    # profile_image: ProfileImageOut
    verified: bool

    class Config:
        from_attributes = True
