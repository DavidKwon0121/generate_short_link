from fastapi import APIRouter

from src.controllers.dto import GenerateShortUrl
from src.modules.cache import CacheDepends
from src.modules.database import AsyncSessionDepends
from src.services.short_url_service import ShortUrlService

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
    su_serv = ShortUrlService(session, cache)
    return await su_serv._generate_short_id()


@router.get("/r/{short_id}")
async def _router_redirect_short_link(short_id: str, session: AsyncSessionDepends):
    pass
