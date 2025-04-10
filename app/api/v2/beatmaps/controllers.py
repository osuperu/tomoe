from __future__ import annotations

from typing import Any

from api.v2.beatmaps.models import BeatmapScore
from api.v2.beatmaps.models import Mod
from api.v2.beatmaps.models import Score
from common import logger
from common import utils
from common.mods import Mods
from common.utils import GameMode
from common.utils import SubmissionStatus
from errors import ServiceError
from fastapi import APIRouter
from fastapi import Query
from services import maps
from services import scores

router = APIRouter()


@router.get("/api/v2/beatmaps/{beatmap}/scores/users/{user}/all")
async def fetch_user_beatmap_scores(
    beatmap: int,
    user: int,
    legacy_only: str = Query(
        default=None,
        description="Whether or not to exclude lazer scores.",
    ),  # unused
    mode: str | None = Query(
        default=None,
        description="Deprecated. The 'Ruleset' to get scores for. Defaults to beatmap ruleset.",
    ),
    ruleset: str | None = Query(
        default=None,
        description="The 'Ruleset' to get scores for. Defaults to beatmap ruleset.",
    ),
) -> Score | dict[str, list[dict[str, Any]] | str]:
    """
    Fetch beatmap scores for a specific user from the osu! API.

    Parameters:
        beatmap (int): Beatmap ID.
        user (int): User ID.

    Query parameters:
        legacy_only (int, optional): Whether or not to exclude lazer scores. Defaults to 0.
        mode (str, optional): Deprecated. The 'Ruleset' to get scores for. Defaults to beatmap ruleset.
        ruleset (str, optional): The 'Ruleset' to get scores for. Defaults to beatmap ruleset.

    More info: https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores
    """
    _map = await maps.fetch_one(id=beatmap)

    if isinstance(_map, ServiceError):
        return {
            "error": "Specified beatmap difficulty couldn't be found.",
        }

    _scores = await scores.fetch_many(
        map_md5=_map["md5"],
        user_id=user,
        mode=(
            GameMode.from_string(mode)
            if mode is not None
            else GameMode.from_string(ruleset) if ruleset is not None else _map["mode"]
        ),
        score_statuses=[SubmissionStatus.SUBMITTED, SubmissionStatus.BEST],
    )

    if isinstance(_scores, ServiceError):
        return {
            "scores:": [],
        }

    validated_scores = [
        Score.model_validate(
            {
                "accuracy": score["acc"] / 100,
                "best_id": score["id"],
                "created_at": score["play_time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "ended_at": score["play_time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "id": score["id"],
                "max_combo": score["max_combo"],
                "mode": repr(GameMode(score["mode"])),
                "ruleset_id": repr(GameMode(score["mode"])),
                "mode_int": score["mode"],
                "mods": Mods.to_array(score["mods"]),
                "passed": True,  # this should be true for all scores because of the filter applied previously
                "perfect": bool(score["perfect"]),
                "pp": score["pp"],
                "rank": score["grade"],
                "replay": False,  # TODO: add .env with BANCHO_PY_PATH to search for replays
                "score": score["score"],
                "classic_total_score": score["score"],
                "total_score": score["score"],
                "statistics": {
                    "count_100": score["n100"],
                    "count_300": score["n300"],
                    "count_50": score["n50"],
                    "count_geki": score["ngeki"],
                    "count_katu": score["nkatu"],
                    "count_miss": score["nmiss"],
                },
                "maximum_statistics": {
                    "count_100": 0,
                    "count_300": 0,
                    "count_50": 0,
                    "count_geki": 0,
                    "count_katu": 0,
                    "count_miss": 0,
                },
                "type": "score_best_osu",  # TODO: to be implemented
                "user_id": score["userid"],
                "current_user_attributes": {
                    "pin": None,
                },
            },
        )
        for score in _scores
    ]

    return {
        "scores": [score.model_dump() for score in validated_scores],
    }


@router.get("/api/v2/beatmaps/{beatmap}/scores")
async def fetch_beatmap_scores(
    beatmap: int,
    legacy_only: int | bool | None = Query(
        description="Whether or not to exclude lazer scores.",
    ),  # unused
    mode: str | None = Query(
        default=None,
        description="Deprecated. The 'Ruleset' to get scores for. Defaults to beatmap ruleset.",
    ),
    mods: list[Mod] | None = Query(
        default=None,
        description="List of mods to filter by.",
    ),  # TODO: to be implemented
    type: str | None = Query(
        default=None,
        description="Beatmap score ranking type",
    ),  # unused for now
) -> BeatmapScore | dict[str, list[dict[str, Any]] | str]:
    _map = await maps.fetch_one(id=beatmap)

    if isinstance(_map, ServiceError):
        return {
            "error": "Specified beatmap difficulty couldn't be found.",
        }

    _scores = await scores.fetch_many(
        map_md5=_map["md5"],
        mode=(GameMode.from_string(mode) if mode is not None else _map["mode"]),
        score_statuses=[SubmissionStatus.SUBMITTED, SubmissionStatus.BEST],
        sort_by="score",
        # TODO: pass mods as a parameter
    )

    if isinstance(_scores, ServiceError):
        return {
            "scores:": [],
        }

    return BeatmapScore.model_validate(
        {
            "score_count": 0,  # TODO: to be implemented
            "scores": [
                Score.model_validate(
                    {
                        "accuracy": score["acc"] / 100,
                        "best_id": score["id"],
                        "created_at": score["play_time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "ended_at": score["play_time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "id": score["id"],
                        "max_combo": score["max_combo"],
                        "mode": repr(GameMode(score["mode"])),
                        "ruleset_id": repr(GameMode(score["mode"])),
                        "mode_int": score["mode"],
                        "mods": Mods.to_array(score["mods"]),
                        "passed": True,  # this should be true for all scores because of the filter applied previously
                        "perfect": bool(score["perfect"]),
                        "pp": score["pp"],
                        "rank": score["grade"],
                        "replay": False,  # TODO: add .env with BANCHO_PY_PATH to search for replays
                        "score": score["score"],
                        "classic_total_score": score["score"],
                        "total_score": score["score"],
                        "statistics": {
                            "count_100": score["n100"],
                            "count_300": score["n300"],
                            "count_50": score["n50"],
                            "count_geki": score["ngeki"],
                            "count_katu": score["nkatu"],
                            "count_miss": score["nmiss"],
                        },
                        "maximum_statistics": {
                            "count_100": 0,
                            "count_300": 0,
                            "count_50": 0,
                            "count_geki": 0,
                            "count_katu": 0,
                            "count_miss": 0,
                        },
                        "type": "score_best_osu",  # TODO: to be implemented
                        "user_id": score["userid"],
                        "current_user_attributes": {
                            "pin": None,
                        },
                    },
                )
                for score in _scores
            ],
        },
    )
