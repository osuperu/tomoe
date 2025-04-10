from __future__ import annotations

from common import logger
from errors import ServiceError
from repositories import maps
from repositories.maps import Map


async def fetch_one(id: int) -> Map | ServiceError:
    try:
        map = await maps.fetch_one(id)
    except Exception as exc:
        logger.error("Failed to fetch map", exc_info=exc)
        return ServiceError.INTERNAL_SERVER_ERROR

    if map is None:
        return ServiceError.MAPS_NOT_FOUND

    return map


async def fetch_many(
    server: str | None = None,
    set_id: int | None = None,
    mode: int | None = None,
) -> list[Map] | ServiceError:
    try:
        _maps = await maps.fetch_many(
            server=server,
            set_id=set_id,
            mode=mode,
        )
    except Exception as exc:
        logger.error("Failed to fetch maps", exc_info=exc)
        return ServiceError.INTERNAL_SERVER_ERROR

    return _maps
