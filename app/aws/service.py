import uuid
from loguru import logger

import aioboto3
from fastapi import APIRouter, File
from botocore.config import Config
from botocore.exceptions import ClientError

from core.config import settings

router = APIRouter(tags=["Files"], prefix="/files")

KB = 1024
MB = KB * 1024

ALLOWED_FILE_TYPES = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = MB * 3


# # singleton class for AWS services
class AwsS3Service:
    """
    Singleton class for interacting with AWS S3 services.

    This class manages interactions with Amazon S3 for tasks such as generating
    pre-signed URLs, uploading files, and ensuring that file types and sizes
    are within specified limits.

    Attributes:
        __session (aioboto3.Session): An aioboto3 session for interacting with AWS services.
        __profile_bucket_name (str): The name of the bucket for profile images.
        __profile_default_image (str): The name of the default profile image.

    """
    __instance = None

    __session: aioboto3.Session
    __profile_bucket_name: str
    __profile_default_image: str

    def __new__(cls):
        """
        Initialize an instance of AwsS3Service.

        Returns:
            AwsS3Service: An instance of the AwsS3Service class.

        """
        if AwsS3Service.__instance is None:
            AwsS3Service.__instance = super().__new__(cls)
            cls.__profile_bucket_name = settings.aws_s3_profile_image_bucket
            cls.__profile_default_image = settings.default_profile_image
            cls.__session = aioboto3.Session(region_name='eu-north-1',
                                             aws_access_key_id=settings.aws_access_key,
                                             aws_secret_access_key=settings.aws_secret_access_key)
        return AwsS3Service.__instance

    def __client(self):
        """
        Get an AWS S3 client.

        Returns:
            botocore.client.BaseClient: An AWS S3 client instance.

        """
        return self.__session.client(service_name="s3",
                                     config=Config(signature_version='s3v4'),
                                     endpoint_url='https://s3.eu-north-1.amazonaws.com')

    async def generate_profile_presigned_url(self, object_name: str) -> str:
        """
        Generate a pre-signed URL for accessing a profile image.

        Args:
            object_name (str): The name of the S3 object (file).

        Returns:
            str: The pre-signed URL.

        """
        return await self.__create_presigned_url(object_name, self.__profile_bucket_name)

    async def upload_profile_image(self, file_object: File, provided_filename: str) -> str:
        """
        Upload a profile image to AWS S3.

        Args:
            file_object (File): The file object to be uploaded.
            provided_filename (str): The original filename provided.

        Returns:
            str: The new filename of the uploaded file on S3.

        """
        return await self.__upload_file_to_s3(file_object, provided_filename, self.__profile_bucket_name)

    async def __create_presigned_url(self, object_name: str, bucket_name: str, expires_in: int = 3600) -> str:
        """
        Create a pre-signed URL for accessing an S3 object.

        Args:
            object_name (str): The name of the S3 object.
            bucket_name (str): The name of the S3 bucket.
            expires_in (int): The duration of validity for the URL.

        Returns:
            str: The pre-signed URL.

        Raises:
            ClientError: If an error occurs during URL generation.

        """
        try:
            async with self.__client() as s3:
                url = await s3.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket_name,
                                                              'Key': object_name},
                                                      ExpiresIn=expires_in)
                return url
        except ClientError as e:
            logger.error(e)
            raise ClientError

    async def __upload_file_to_s3(self, file_object: File, provided_filename: str, bucket_name: str) -> str:
        """
        Upload a file to AWS S3.

        Args:
            file_object (File): The file object to be uploaded.
            provided_filename (str): The original filename provided.
            bucket_name (str): The name of the S3 bucket.

        Returns:
            str: The new filename of the uploaded file on S3.

        """
        new_filename = self.__generate_unique_filename(provided_filename)
        async with self.__client() as s3:
            await s3.upload_fileobj(file_object, bucket_name, new_filename)
        return new_filename

    def __generate_unique_filename(self, provided_filename):
        """
        Generate a unique filename for uploaded files.

        Args:
            provided_filename (str): The original filename provided.

        Returns:
            str: The generated unique filename.

        """
        return f"{str(uuid.uuid4())}.{self.__get_file_type(provided_filename)}"

    @logger.catch
    def __get_file_type(self, filename: str):
        """
        Get the file type (extension) from a filename.

        Args:
            filename (str): The filename from which to extract the file type.

        Returns:
            str: The file type (extension) in lowercase.

        """
        return "." in filename and filename.rsplit(".", 1)[1].lower()

    @logger.catch
    def is_file_type_allowed(self, filename: str):
        """
        Check if the file type is allowed.

        Args:
            filename (str): The filename to check.

        Returns:
            bool: True if the file type is allowed, False otherwise.

        """
        return self.__get_file_type(filename) in ALLOWED_FILE_TYPES

    @logger.catch
    def is_file_size_allowed(self, size: int):
        """
        Check if the file size is within allowed limits.

        Args:
            size (int): The size of the file in bytes.

        Returns:
            bool: True if the file size is allowed, False otherwise.

        """
        return MAX_FILE_SIZE > size
