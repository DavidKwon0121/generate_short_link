from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import secret_settings

database_url = URL(
    drivername="mysql+aiomysql",
    username=secret_settings.mysql_username,
    password=secret_settings.mysql_password,
    host=secret_settings.mysql_host,
    port=secret_settings.mysql_port,
    database=secret_settings.mysql_dbname,
    query={"charset": "utf8mb4"},
)

engine = create_async_engine(
    database_url, pool_recycle=300, pool_size=10, max_overflow=100
)

SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def session():
    async with SessionFactory() as async_session:
        yield async_session


async def database():
    async with session() as s:
        yield s


AsyncSessionDepends = Annotated[AsyncSession, Depends(database)]