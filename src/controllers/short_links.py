from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse, RedirectResponse

from src.controllers.dto import GenerateShortUrl
from src.modules.cache import CacheDepends
from src.modules.database import AsyncSessionDepends
from src.modules.utils import is_url_or_raise
from src.services.short_url_service import ShortUrlService

router = APIRouter(prefix="/short-links")


@router.post("")
async def _router_create(
    data: GenerateShortUrl, session: AsyncSessionDepends, cache: CacheDepends
):
    url = data.url
    is_url_or_raise(url)
    ss = ShortUrlService(session, cache)
    ret = await ss.find_exist(url)
    if not ret:
        ret = ss.create(url)
        await session.commit()
    return JSONResponse(content=ret.return_camelize())


@router.get("/{short_id}")
async def _router_get(short_id: str, session: AsyncSessionDepends, cache: CacheDepends):
    ss = ShortUrlService(session, cache)
    ret = await ss.get(short_id)
    if ret:
        return JSONResponse(content=ret.return_camelize())

    raise HTTPException(status_code=404, detail="Unknown short id")


@router.get("/r/{short_id}")
async def _router_redirect(
    short_id: str, session: AsyncSessionDepends, cache: CacheDepends
):
    ss = ShortUrlService(session, cache)
    ret = await ss.get(short_id)
    if ret:
        return RedirectResponse(url=ret.url_str, status_code=302)

    raise HTTPException(status_code=404, detail="Unknown short id")
