from loguru import logger
from pydantic import  Field, EmailStr
from pydantic_settings import BaseSettings

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG",
           rotation="10 MB", compression="zip", serialize=True, enqueue=True)


# get environment variables from file
class Settings(BaseSettings):
    pg_database_hostname: str
    pg_database_port: str
    pg_database_password: str
    pg_database_name: str
    pg_database_username: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_token_expire_minutes: int

    redis_host: str
    redis_port: str
    redis_celery_broker_db: str
    redis_celery_backend_db: str

    s3_access_key: str
    s3_secret_access_key: str
    s3_profile_image_bucket: str
    default_profile_image: str

    mongo_username: str = Field(..., env="mongo_username")
    mongo_password: str = Field(..., env="mongo_password")
    mongo_cluster_name: str = Field(..., env="mongo_cluster_name")
    mongo_chat_database_name: str = Field(..., env="mongo_chat_database_name")
    mongo_messages_collection_name: str = Field(..., env="mongo_messages_collection_name")

    email_host: str = Field(..., env="email_host")
    email_port: str = Field(..., env="email_port")
    email_username: str = Field(..., env="email_username")
    email_password: str = Field(..., env="email_password")
    email_from: EmailStr = Field(..., env="email_from")

    spotify_client_id: str = Field(..., env="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str = Field(..., env="SPOTIFY_CLIENT_SECRET")
    spotify_redirect_uri: str = Field(..., env="SPOTIFY_REDIRECT_URI")
    spotify_scopes: list[str] = Field(..., env="SPOTIFY_SCOPES")

    class Config:
        env_file = ".env-dev"


settings = Settings()
