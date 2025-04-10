from __future__ import annotations

from typing import Any

from common import clients
from common import settings
from httpx import HTTPError


async def request(endpoint: str) -> dict[str, Any] | None:
    url = f"https://api.{settings.DOMAIN}/{endpoint}"
    try:
        response = await clients.http_client.get(url)
        response.raise_for_status()
    except HTTPError:
        return None
    else:
        data: dict[str, Any] = response.json()
        return data
