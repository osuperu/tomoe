from __future__ import annotations

from datetime import datetime
from typing import TypedDict
from typing import cast

from common import clients

READ_PARAMS = """
    id,
    name,
    tag,
    owner,
    created_at
"""


class Clan(TypedDict):
    id: int
    name: str
    tag: str
    owner: int
    created_at: datetime


async def fetch_one(id: int) -> Clan | None:
    clan = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM clans
            WHERE id = :id
        """,
        values={"id": id},
    )
    return cast(Clan, clan) if clan is not None else None
