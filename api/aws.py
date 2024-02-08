from typing import Annotated

from loguru import logger
from fastapi import status, APIRouter, UploadFile, HTTPException, File, Depends

from app.aws import schemas
from app.aws.service import AwsS3Service

aws_router = APIRouter(tags=["Files"], prefix="/files")


@aws_router.post("/profile", status_code=status.HTTP_201_CREATED, response_model=schemas.ImageOut)
async def upload_profile_image(image: Annotated[UploadFile, File()],
                               s3: Annotated[AwsS3Service, Depends()]):
    """
    Uploads an image and returns the presigned URL and new filename of the uploaded image.

    Args:
        image (UploadFile): The uploaded image file.
        s3 (AwsS3Service): The AWS S3 service instance obtained from the dependency.

    Returns:
        ImageOut: The response model containing the URL and filename of the uploaded image.

    Raises:
        HTTPException: If the file size is too large or if the file type is not supported.

    """
    if not s3.is_file_size_allowed(image.size):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="File is too large")
    if not s3.is_file_type_allowed(image.filename):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="File type not supported")

    new_filename = await s3.upload_profile_image(file_object=image.file, provided_filename=image.filename)
    presigned_url = await s3.generate_profile_presigned_url(object_name=new_filename)

    return schemas.ImageOut(filename=new_filename, url=presigned_url)


@aws_router.get("/profile", response_model=schemas.ImageOut)
async def get_presigned_url_profile_image(filename: str, s3: Annotated[AwsS3Service, Depends()]):
    """
    Retrieves the presigned URL and filename of a profile image.

    Args:
        filename (str): The filename of the profile image.
        s3 (AwsS3Service): The AWS S3 service instance obtained from the dependency.

    Returns:
        ImageOut: The response model containing the URL and filename of the profile image.

    """
    presigned_url = await s3.generate_profile_presigned_url(object_name=filename)
    return schemas.ImageOut(filename=filename, url=presigned_url)
