from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.chat.models import Message
from core.config import settings

MONGO_DATABASE_URI = f"mongodb+srv://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_cluster_name}.oxr76f3.mongodb.net/?retryWrites=true&w=majority"


def get_motor_client():
    return AsyncIOMotorClient(MONGO_DATABASE_URI, uuidRepresentation="standard")


async def init_db_beanie():
    client = get_motor_client()

    await init_beanie(database=client[settings.mongo_chat_database_name], document_models=[Message])


async def get_message_collection() -> AsyncIOMotorCollection:
    try:
        client = get_motor_client()
        db = client[settings.mongo_chat_database_name]
        return db[settings.mongo_messages_collection_name]
    except Exception:
        raise ConnectionError("Error in connection to Chat DB")