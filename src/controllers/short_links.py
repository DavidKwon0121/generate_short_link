from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse, RedirectResponse

from src.controllers.dto import GenerateShortLink
from src.modules.cache import CacheDepends
from src.modules.database import AsyncSessionDepends
from src.modules.utils import is_url_or_raise
from src.services.short_link_service import ShortLinkService

router = APIRouter(prefix="/short-links")


@router.post("")
async def _router_create(
    data: GenerateShortLink, session: AsyncSessionDepends, cache: CacheDepends
):
    url = data.url
    is_url_or_raise(url)
    ss = ShortLinkService(session, cache)
    ret = ss.create(url)
    await session.commit()
    return JSONResponse(content=ret.return_camelize())


@router.get("/{short_id}")
async def _router_get(short_id: str, session: AsyncSessionDepends, cache: CacheDepends):
    short_link = ShortLinkService(session, cache)
    ret = await short_link.get(short_id)
    if ret:
        return JSONResponse(content=ret.return_camelize())

    raise HTTPException(status_code=404, detail="Unknown short id")


@router.get("/r/{short_id}")
async def _router_redirect(
    short_id: str, session: AsyncSessionDepends, cache: CacheDepends
):
    short_link = ShortLinkService(session, cache)
    ret = await short_link.get(short_id)
    if ret:
        return RedirectResponse(url=ret.url_str, status_code=302)

    raise HTTPException(status_code=404, detail="Unknown short id")
