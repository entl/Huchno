from typing import Sequence

import redis.client
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.location.models import Location


class SqlAlchemyLocationRepository:
    @classmethod
    async def find_by_user_id(cls, user_id: str, session: AsyncSession) -> Location | None:
        query = select(Location).filter(Location.user_id == user_id)
        return (await session.execute(query)).scalars().first()

    @classmethod
    async def add(cls, user_id, longitude, latitude, session: AsyncSession) -> Location:
        location = Location(user_id=user_id, longitude=longitude, latitude=latitude)
        session.add(location)
        await session.commit()
        await session.flush()
        return location

    @classmethod
    async def find_bulk_by_user_ids(cls, user_ids: list[str], session: AsyncSession) -> Sequence[Location]:
        query = select(Location).filter(Location.user_id.in_(user_ids))
        return (await session.execute(query)).scalars().all()

    @classmethod
    async def update(cls, user_id: str, longitude: float, latitude: float, session: AsyncSession) -> Location:
        query = select(Location).filter(Location.user_id == user_id)
        location = (await session.execute(query)).scalars().first()
        location.longitude = longitude
        location.latitude = latitude
        await session.commit()
        await session.flush()
        return location



