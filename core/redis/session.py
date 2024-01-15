from typing import AsyncGenerator

import redis.asyncio as redis
from redis.asyncio import Redis

from core.config import settings


def get_redis_connection():
    pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db="2")
    client = redis.Redis.from_pool(pool)
    return client
