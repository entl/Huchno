from pydantic import BaseModel, HttpUrl
from core.config import settings


class ImageOut(BaseModel):
    """
    Model for representing an image with its URL and filename.

    Attributes:
        url (HttpUrl): The URL of the image.
        filename (str): The filename of the image. Defaults to the default profile image filename from AWS settings.

    """
    url: HttpUrl
    filename: str = settings.default_profile_image
