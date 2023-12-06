from typing import Annotated
import redis
from fastapi import Depends
from redlock import Redlock

from src.config import secret_settings

redis_url = f"redis://{secret_settings.redis_host}:{secret_settings.redis_port}"
pool = redis.ConnectionPool.from_url(redis_url)


def get_cache():
    cache = redis.StrictRedis.from_pool(pool)
    try:
        yield cache
    finally:
        cache.close()


class RedlockManager:
    lock_ttl = 1000
    retry_count = 3
    retry_delay = 100

    def __init__(self, client):
        self.redlock = Redlock(
            [client],
            retry_count=self.retry_count,
            retry_delay=self.retry_delay,
        )

    def get_lock(self, key: str):
        lock = self.redlock.lock(
            f"lock:{key}",
            self.lock_ttl,
        )
        if lock:
            return lock
        raise Exception("Fail to get redlock")

    def unlock(self, lock):
        self.redlock.unlock(lock)


CacheDepends = Annotated[redis.Redis, Depends(get_cache)]
