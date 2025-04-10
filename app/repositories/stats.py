from __future__ import annotations

from typing import TypedDict
from typing import cast

from common import clients

READ_PARAMS = """
    id,
    mode,
    tscore,
    rscore,
    pp,
    plays,
    playtime,
    acc,
    max_combo,
    total_hits,
    replay_views,
    xh_count,
    x_count,
    sh_count,
    s_count,
    a_count
"""


class Stat(TypedDict):
    id: int
    mode: int
    tscore: int
    rscore: int
    pp: int
    plays: int
    playtime: int
    acc: float
    max_combo: int
    total_hits: int
    replay_views: int
    xh_count: int
    x_count: int
    sh_count: int
    s_count: int
    a_count: int


async def fetch_one(user_id: int, mode: int) -> Stat | None:
    stats = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM stats
            WHERE id = :id AND mode = :mode
        """,
        values={"id": user_id, "mode": mode},
    )
    return cast(Stat, stats) if stats is not None else None
