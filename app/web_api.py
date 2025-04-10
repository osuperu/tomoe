from __future__ import annotations

import atexit
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from api import rest_api_router
from common import lifecycle
from common import logger
from common import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger.configure_logging(
    app_env=settings.APP_ENV,
    log_level=settings.APP_LOG_LEVEL,
)
logger.overwrite_exception_hook()
atexit.register(logger.restore_exception_hook)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    await lifecycle.start()
    yield
    await lifecycle.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.host(settings.DOMAIN if settings.DOMAIN else settings.APP_HOST, rest_api_router)

# when running for local dev, allow developers to use
# http://localhost/ or http://127.0.0.1 to test the API
# more easily to avoid the requirement of manualy overriding DNS
if settings.APP_ENV == "local":
    app.host("localhost", rest_api_router)
    app.host("127.0.0.1", rest_api_router)
