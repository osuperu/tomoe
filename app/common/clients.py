from __future__ import annotations

from adapters.database import Database
from adapters.redis import Redis
from httpx import AsyncClient

database: Database
redis: Redis
http_client = AsyncClient()
