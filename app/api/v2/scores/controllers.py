from __future__ import annotations

from typing import Literal

from common import logger
from common import utils
from common.utils import GameMode
from errors import ServiceError
from fastapi import APIRouter
from fastapi import Query
from services import scores

router = APIRouter()


@router.get("/api/v2/scores")
async def fetch_scores(
    ruleset: Literal["osu", "taiko", "fruits", "mania"] = Query(
        default="osu",
        description="Ruleset of the scores to be returned.",
    ),
    cursor_string: str | None = Query(
        default=None,
        description="Cursor string for pagination.",
    ),
):
    """
    Returns all passed scores. Up to 1000 scores will be returned in order of oldest to latest.
    Most recent scores will be returned if cursor_string parameter is not specified.

    Obtaining new scores that arrived after the last request can be done by passing cursor_string parameter from the previous request.

    Query parameters:
        ruleset (str, optional): The Ruleset to get scores for.
        cursor_string (str, optional): Next set of scores.

    More info: https://osu.ppy.sh/docs/index.html#get-scores97
    """
    _scores = await scores.fetch_many(
        map_md5=None,
        user_id=None,
        mode=GameMode.from_string(ruleset),
        score_statuses=None,
        map_statuses=None,
        sort_by="play_time",
        order="asc",
        page=None,
        page_size=None,
    )

    if isinstance(_scores, ServiceError):
        return []

    logger.info(_scores)
    return _scores
