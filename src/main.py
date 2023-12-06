from fastapi import APIRouter, FastAPI, Depends
from starlette.responses import PlainTextResponse

from src.controllers import ROUTERS
from src.models.database import AsyncSessionDepends
from src.services.request_service import RequestService

router = APIRouter()


@router.get("/", response_model=None)
async def hello(
    session: AsyncSessionDepends,
    request: RequestService = Depends(),
):
    return PlainTextResponse(
        f"{request.base_url}\n"
        f"{request.user_agent}\n"
        f"{request.ip_address}\n"
        f"{request.browser}\n"
        f"{request.device}\n"
        f"{request.os}\n"
        f"session connected: {session.is_active}"
    )


app = FastAPI()
app.include_router(router)
for _router in ROUTERS:
    app.include_router(_router)
