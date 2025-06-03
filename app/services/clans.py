from __future__ import annotations

from common import logger
from errors import ServiceError
from repositories import clans
from repositories.clans import Clan


async def fetch_one(id: int) -> Clan | ServiceError:
    try:
        clan = await clans.fetch_one(id)
    except Exception as exc:
        logger.error("Failed to fetch clan", exc_info=exc)
        return ServiceError.INTERNAL_SERVER_ERROR

    if clan is None:
        return ServiceError.CLANS_NOT_FOUND

    return clan
