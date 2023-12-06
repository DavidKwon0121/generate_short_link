import asyncio

import pytest
import redis
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import URL, event
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)

from src.config import secret_settings
from src.main import app
from src.modules.database import database, Base


@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def async_engine() -> AsyncEngine:
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

    yield engine


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def session(async_engine):
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()

        # 전체 스키마 생성
        try:
            await conn.run_sync(Base.metadata.create_all)
        except:
            pass

        async_session = AsyncSession(
            conn,
            expire_on_commit=False,
            autoflush=False,
        )

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return

            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield async_session
        await conn.rollback()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop


@pytest.fixture(scope="function")
def cache():
    cache = redis.StrictRedis.from_pool(
        redis.ConnectionPool.from_url(
            f"redis://{secret_settings.redis_host}:{secret_settings.redis_port}"
        )
    )
    yield cache
    cache.flushdb()
    cache.close()


@pytest.fixture(scope="function")
async def client(session, cache):
    def override_database():
        return session

    def override_cache():
        return cache

    app.dependency_overrides[database] = override_database
    from src.modules.cache import get_cache

    app.dependency_overrides[get_cache] = override_cache
    async with AsyncClient(app=app, base_url="http://test") as ac, LifespanManager(app):
        yield ac

    del app.dependency_overrides[database]
    del app.dependency_overrides[get_cache]
