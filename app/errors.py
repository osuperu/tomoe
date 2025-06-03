from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    INTERNAL_SERVER_ERROR = "global.internal_server_error"

    USERS_NOT_FOUND = "users.not_found"

    MAPS_NOT_FOUND = "maps.not_found"

    CLANS_NOT_FOUND = "clans.not_found"
