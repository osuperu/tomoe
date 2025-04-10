from __future__ import annotations

from datetime import datetime
from typing import Literal
from typing import TypedDict
from typing import cast

from common import clients
from services import maps

READ_PARAMS = """\
    s.id,
    s.map_md5,
    s.score,
    s.pp,
    s.acc,
    s.max_combo,
    s.mods,
    s.n300,
    s.n100,
    s.n50,
    s.nmiss,
    s.ngeki,
    s.nkatu,
    s.grade,
    s.status,
    s.mode,
    s.play_time,
    s.time_elapsed,
    s.client_flags,
    s.userid,
    s.perfect,

    -- beatmap fields
    m.id AS beatmap_id,
    m.artist,
    m.title,
    m.version
"""


class Score(TypedDict):
    id: int
    map_md5: str
    score: int
    pp: float
    acc: float
    max_combo: int
    mods: int
    n300: int
    n100: int
    n50: int
    nmiss: int
    ngeki: int
    nkatu: int
    grade: str
    status: int
    mode: int
    play_time: datetime
    time_elapsed: int
    client_flags: int
    userid: int
    perfect: bool

    # beatmap fields
    beatmap_id: int
    artist: str
    title: str
    version: str


async def fetch_many(
    map_md5: str | None = None,
    user_id: int | None = None,
    mode: int | None = None,
    score_statuses: list[int] | None = None,
    map_statuses: list[int] | None = None,
    sort_by: Literal[
        "score",
        "pp",
        "acc",
        "play_time",
    ] = "pp",
    order: Literal["asc", "desc"] = "desc",
    page: int | None = None,
    page_size: int | None = None,
) -> list[Score]:
    query = f"""
        SELECT {READ_PARAMS}
        FROM scores s
        LEFT JOIN maps m ON s.map_md5 = m.md5
        WHERE s.map_md5 = COALESCE(:map_md5, s.map_md5)
        AND s.userid = COALESCE(:user_id, s.userid)
        AND s.mode = COALESCE(:mode, s.mode)
    """
    values = {
        "map_md5": map_md5,
        "user_id": user_id,
        "mode": mode,
    }

    if score_statuses is not None:
        placeholders = ", ".join(
            [f":score_status_{i}" for i in range(len(score_statuses))],
        )
        values |= {
            f"score_status_{i}": status for i, status in enumerate(score_statuses)
        }
        query += f" AND s.status IN ({placeholders})"

    if map_statuses is not None:
        placeholders = ", ".join([f":map_status_{i}" for i in range(len(map_statuses))])
        values |= {f"map_status_{i}": status for i, status in enumerate(map_statuses)}
        query += f" AND m.status IN ({placeholders})"

    query += f" ORDER BY {sort_by} {order.upper()}"

    if page is not None and page_size is not None:
        query += f"""\
            LIMIT :page_size
            OFFSET :offset
        """
        values["page_size"] = page_size
        values["offset"] = (page - 1) * page_size

    scores = await clients.database.fetch_all(query, values)
    return [cast(Score, score) for score in scores] if scores else []
