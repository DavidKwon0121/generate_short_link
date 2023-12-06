from fastapi import APIRouter

from src.controllers.dto import GenerateShortUrl
from src.modules.cache import CacheDepends
from src.modules.database import AsyncSessionDepends

router = APIRouter(prefix="/short-links")


@router.post("")
async def _router_generate_short_link(
    data: GenerateShortUrl, session: AsyncSessionDepends, cache: CacheDepends
):
    pass


@router.get("/{short_id}")
async def _router_get_short_link(
    short_id: int, session: AsyncSessionDepends, cache: CacheDepends
):
    key = "short_id"
    print(f"{key}: ", short_id)
    await cache.set(key, short_id)
    print(await cache.get(key))
    return await cache.get(key)


@router.get("/r/{short_id}")
async def _router_redirect_short_link(short_id: str, session: AsyncSessionDepends):
    pass
