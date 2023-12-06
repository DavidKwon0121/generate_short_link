from fastapi import APIRouter

from src.controllers.dto import GenerateShortUrl
from src.models.database import AsyncSessionDepends

router = APIRouter(prefix="/short-links")


@router.post("")
async def _router_generate_short_link(
    data: GenerateShortUrl, session: AsyncSessionDepends
):
    pass


@router.get("/{short_id}")
async def _router_get_short_link(short_id: str, session: AsyncSessionDepends):
    pass


@router.get("/r/{short_id}")
async def _router_redirect_short_link(short_id: str, session: AsyncSessionDepends):
    pass
