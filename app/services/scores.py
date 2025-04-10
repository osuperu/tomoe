from __future__ import annotations

from typing import Literal

from common import logger
from errors import ServiceError
from repositories import scores
from repositories.scores import Score


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
) -> list[Score] | ServiceError:
    try:
        _scores = await scores.fetch_many(
            map_md5=map_md5,
            user_id=user_id,
            mode=mode,
            score_statuses=score_statuses,
            map_statuses=map_statuses,
            sort_by=sort_by,
            order=order,
            page=page,
            page_size=page_size,
        )
    except Exception as exc:
        logger.error("Failed to fetch scores", exc_info=exc)
        return ServiceError.INTERNAL_SERVER_ERROR

    return _scores
