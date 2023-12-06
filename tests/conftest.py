import pytest
import redis
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)

from src.config import secret_settings
from src.main import app
from src.modules.database import Base


@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def async_engine_conn():
    engine = create_async_engine(
        URL.create(
            drivername="mysql+aiomysql",
            username=secret_settings.mysql_username,
            password=secret_settings.mysql_password,
            host=secret_settings.mysql_host,
            port=secret_settings.mysql_port,
            database=secret_settings.mysql_dbname,
            query={"charset": "utf8mb4"},
        ),
    )
    async with engine.begin() as conn:
        yield conn
        for table in Base.metadata.tables.values():
            await conn.execute(table.delete())


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def db(async_engine_conn):
    async for conn in async_engine_conn:
        async_session = AsyncSession(
            conn,
            expire_on_commit=False,
            autoflush=False,
        )
        yield async_session
        await async_session.aclose()


@pytest.fixture(scope="function", autouse=True)
def redis_cache():
    cache = redis.StrictRedis.from_pool(
        redis.ConnectionPool.from_url(
            f"redis://{secret_settings.redis_host}:{secret_settings.redis_port}"
        )
    )
    yield cache
    cache.flushdb()
    cache.close()


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def client(db, redis_cache):
    from src.modules.database import database
    from src.modules.cache import get_cache

    async for session in db:

        def override_database():
            return session

        def override_cache():
            return redis_cache

        app.dependency_overrides[database] = override_database
        app.dependency_overrides[get_cache] = override_cache

        async with AsyncClient(app=app, base_url="http://test") as ac, LifespanManager(
            app
        ):
            yield ac

        del app.dependency_overrides[database]
        del app.dependency_overrides[get_cache]
