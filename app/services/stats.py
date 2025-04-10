from __future__ import annotations

from common import logger
from errors import ServiceError
from repositories import stats
from repositories.stats import Stat


async def fetch_one(user_id: int, mode: int) -> Stat | ServiceError:
    try:
        user_stats = await stats.fetch_one(user_id, mode)
    except Exception as exc:
        logger.error("Failed to fetch user stats", exc_info=exc)
        return ServiceError.INTERNAL_SERVER_ERROR

    if user_stats is None:
        return ServiceError.USERS_NOT_FOUND

    return user_stats
