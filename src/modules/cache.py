from typing import Annotated
import redis.asyncio as redis
from fastapi import Depends

from src.config import secret_settings

pool = redis.ConnectionPool.from_url(
    f"redis://{secret_settings.redis.host}:{secret_settings.redis.port}"
)


def get_cache():
    return redis.Redis.from_pool(pool)


async def cache_depends():
    cache = get_cache()
    try:
        yield cache
    finally:
        await cache.aclose()


CacheDepends = Annotated[redis.Redis, Depends(cache_depends)]
