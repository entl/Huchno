from asyncpg import UniqueViolationError
from pydantic import UUID4
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import async_session_factory
from core.redis.session import get_redis_connection

from core.config import settings


from . import schemas
from .repository import SqlAlchemyLocationRepository, RedisPubSubRepository


class LocationService:
    def __init__(self):
        self.sql_alchemy_location_repository = SqlAlchemyLocationRepository()
        self.redis_pub_sub_repository = RedisPubSubRepository()
        self.redis_connection = get_redis_connection()

    async def get_location_by_user_id(self, user_id: str) -> schemas.LocationOut:
        async with async_session_factory() as session:
            location_in_db = await self.sql_alchemy_location_repository.find_by_user_id(user_id=user_id, session=session)
            return schemas.LocationOut.model_validate(location_in_db)

    async def set_or_update_location_by_user_id(self, location: schemas.LocationBase, user_id: UUID4) -> schemas.LocationOut:
        try:
            return await self.set_location_by_user_id(location=location, user_id=user_id)
        except IntegrityError:
            return await self.update_location_by_user_id(location=location, user_id=user_id)

    async def set_location_by_user_id(self, location: schemas.LocationBase, user_id: UUID4) -> schemas.LocationOut:
        async with async_session_factory() as session:
            location_in_db = await self.sql_alchemy_location_repository.add(
                user_id=str(user_id), longitude=location.longitude, latitude=location.latitude, session=session
            )
            return schemas.LocationOut.model_validate(location_in_db)
    
    async def update_location_by_user_id(self, location: schemas.LocationBase, user_id: UUID4) -> schemas.LocationOut:
        async with async_session_factory() as session:
            location_in_db = await self.sql_alchemy_location_repository.update(
                user_id=str(user_id), longitude=location.longitude, latitude=location.latitude, session=session
            )
            return schemas.LocationOut.model_validate(location_in_db)

    async def get_all_friends_locations(self, friends_ids: list[str]) -> list[schemas.LocationOut]:
        async with async_session_factory() as session:
            locations = await self.sql_alchemy_location_repository.find_bulk_by_user_ids(user_ids=friends_ids, session=session)
            return [schemas.LocationOut.model_validate(location) for location in locations]

    async def publish_location(self, location: schemas.LocationBase, user_id: UUID4):
        modified_location = schemas.LocationInRedis(user_id=user_id, longitude=location.longitude, latitude=location.latitude)

        await self.redis_pub_sub_repository.publish(
            channel=f"channel:{settings.redis_location_channel}",
            message=modified_location.model_dump_json(),
            redis=self.redis_connection
        )

    async def subscribe_location_with_user_id(self, user_id: str):
        pubsub = await self.redis_pub_sub_repository.subscribe(
            channel=f"channel:{settings.redis_location_channel}",
            redis=self.redis_connection
        )
        while True:
            location = await pubsub.get_message(ignore_subscribe_messages=True)
            if location is not None and user_id in location["data"].decode():
                yield location["data"].decode()

