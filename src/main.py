from contextlib import asynccontextmanager

from fastapi import FastAPI

from acl.client import OpenFgaClientSingleton
from auth.api.v1.router import router as auth_router
from board.api.v1.router import router as board_router
from core.error_handler import register_exception_handlers
from invitation.api.v1.router import router as invitation_router
from logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # The shutdown actions.
    await OpenFgaClientSingleton.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(board_router)
app.include_router(invitation_router)

register_exception_handlers(app)
logger.info("Starting API...")
