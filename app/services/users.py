from __future__ import annotations

from typing import Any

from common import logger
from errors import ServiceError
from repositories import users
from repositories.users import User


async def fetch_by_user_id(id: int) -> User | ServiceError:
    try:
        user = await users.fetch_by_user_id(id)
    except Exception as exc:
        logger.error("Failed to fetch account", exc_info=exc)
        return ServiceError.INTERNAL_SERVER_ERROR

    if user is None:
        return ServiceError.USERS_NOT_FOUND

    return user


async def fetch_by_username(username: str) -> User | ServiceError:
    try:
        user = await users.fetch_by_username(username)
    except Exception as exc:
        logger.error("Failed to fetch account", exc_info=exc)
        return ServiceError.INTERNAL_SERVER_ERROR

    if user is None:
        return ServiceError.USERS_NOT_FOUND

    return user
