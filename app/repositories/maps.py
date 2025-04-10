from __future__ import annotations

from datetime import datetime
from typing import TypedDict
from typing import cast

from common import clients

READ_PARAMS = """
    id,
    set_id,
    status,
    md5,
    artist,
    title,
    version,
    creator,
    filename,
    last_update,
    total_length,
    max_combo,
    frozen,
    plays,
    passes,
    mode,
    bpm,
    cs,
    ar,
    od,
    hp,
    diff
"""


class Map(TypedDict):
    id: int
    set_id: int
    status: int
    md5: str
    artist: str
    title: str
    version: str
    creator: str
    filename: str
    last_update: datetime
    total_length: int
    max_combo: int
    frozen: bool
    plays: int
    passes: int
    mode: int
    bpm: float
    cs: float
    ar: float
    od: float
    hp: float
    diff: float


async def fetch_one(id: int) -> Map | None:
    map = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM maps
            WHERE id = :id
        """,
        values={"id": id},
    )
    return cast(Map, map) if map is not None else None


async def fetch_many(
    server: str | None = None,
    set_id: int | None = None,
    mode: int | None = None,
) -> list[Map]:
    maps = await clients.database.fetch_all(
        query=f"""
            SELECT {READ_PARAMS}
            FROM maps
            WHERE server = COALESCE(:server, server)
            AND set_id = COALESCE(:set_id, set_id)
            AND mode = COALESCE(:mode, mode)
        """,
        values={
            "server": server,
            "set_id": set_id,
            "mode": mode,
        },
    )
    return [cast(Map, map) for map in maps]
