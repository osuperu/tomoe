from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Literal

import pycountry
from api.v2.beatmaps.models import Score
from api.v2.users.models import Gamemode
from api.v2.users.models import User
from common import clients
from common import logger
from common import utils
from common.mods import Mods
from common.utils import GameMode
from common.utils import RankedStatus
from common.utils import SubmissionStatus
from errors import ServiceError
from fastapi import APIRouter
from fastapi import Query
from services import scores
from services import stats
from services import users

router = APIRouter()


@router.get("/api/v2/users/{user}")
@router.get("/api/v2/users/{user}/{mode}")
async def fetch_user(
    user: str,
    mode: str = "osu",
    key: str | None = Query(
        default=None,
        description="Type of 'user' passed in URL parameter. Can be either 'id' or 'username'.",
    ),
) -> User | dict[str, str]:
    """
    This endpoint returns the detail of specified user.

    Parameters:
        user (str): Id or @-prefixed username of the user. Previous usernames are also checked in some cases.
        mode (str, optional): User default mode will be used if not specified.
            Valid values are:
            - osu = osu!standard
            - taiko = osu!taiko
            - fruits = osu!catch
            - mania = osu!mania
        key (str, optional): Type of 'user' passed in URL parameter.
            Can be either 'id' or 'username' to limit lookup by their respective type.
            Passing an empty or invalid value will result in an ID lookup followed by a username lookup if not found.
            This parameter has been deprecated. Prefix user parameter with @ instead to lookup by username.

    More info: https://osu.ppy.sh/docs/index.html#get-user
    """
    search_by_id = key == "id" if key is not None else not user.startswith("@")
    mode_int = GameMode.from_string(mode)

    if search_by_id:
        _user = await users.fetch_by_user_id(id=int(user))
    else:
        _user = await users.fetch_by_username(
            username=user[1:] if user.startswith("@") else user,
        )

    if isinstance(_user, ServiceError):
        return {}

    _user_stats = await stats.fetch_one(user_id=_user["id"], mode=mode_int)
    # TODO: fix crash when the user never played in the specified mode
    global_rank = await clients.redis.zrevrank(
        f"bancho:leaderboard:{mode_int}",
        _user["id"],
    )
    country_rank = await clients.redis.zrevrank(
        f"bancho:leaderboard:{mode_int}:{_user['country']}",
        _user["id"],
    )

    if isinstance(_user_stats, ServiceError):
        return {}

    country = pycountry.countries.get(alpha_2=_user["country"])
    assert country is not None

    return User.model_validate(
        {
            "avatar_url": "https://osu.ppy.sh/images/layout/avatar-guest@2x.png",  # TODO: add BANCHO_PY_URL to .env and use it here
            "country_code": _user["country"].upper(),
            "default_group": "default",
            "id": _user["id"],
            "is_active": True,
            "is_bot": True if _user["id"] == 1 else False,
            "is_deleted": False,
            "is_online": True,
            "is_supporter": False,
            "last_visit": datetime.utcfromtimestamp(_user["latest_activity"])
            .replace(tzinfo=timezone.utc)
            .isoformat(),  # TODO: don't use this deprecated method, also check if this is correct
            "pm_friends_only": False,
            "profile_colour": None,
            "username": _user["name"],
            "cover_url": "",
            "discord": None,
            "has_supported": False,
            "interests": "",
            "join_date": datetime.utcfromtimestamp(_user["creation_time"])
            .replace(tzinfo=timezone.utc)
            .isoformat(),  # TODO: don't use this deprecated method, also check if this is correct
            "location": "",
            "max_blocks": 50,
            "max_friends": 250,
            "occupation": "",
            "playmode": mode,
            "playstyle": [],
            "post_count": 0,
            "profile_hue": None,
            "profile_order": [
                "me",
                "recent_activity",
                "top_ranks",
                "medals",
                "historical",
                "beatmaps",
                "kudosu",
            ],
            "title": None,
            "title_url": None,
            "twitter": None,
            "website": None,
            "country": {
                "code": _user["country"].upper(),
                "name": country.name,
            },
            "cover": {
                "custom_url": "",
                "url": "",
                "id": "",
            },
            "kudosu": {
                "available": 420,
                "total": 727,
            },
            "is_restricted": False,
            "account_history": [],
            "active_tournament_banner": None,
            "active_tournament_banners": [],
            "badges": [],
            "beatmap_playcounts_count": 0,
            "comments_count": 0,
            "daily_challenge_user_stats": {
                "daily_streak_best": 0,
                "daily_streak_current": 0,
                "last_update": "2000-01-01T00:00:00+00:00",  # TODO: use datetime
                "last_weekly_streak": "2000-01-01T00:00:00+00:00",  # TODO: use datetime
                "playcount": 0,
                "top_10p_placements": 0,
                "top_50p_placements": 0,
                "user_id": _user["id"],
                "weekly_streak_best": 0,
                "weekly_streak_current": 0,
            },
            "favourite_beatmapset_count": 0,
            "follower_count": 0,
            "graveyard_beatmapset_count": 0,
            "groups": [],
            "guest_beatmapset_count": 0,
            "loved_beatmapset_count": 0,
            "mapping_follower_count": 0,
            "monthly_playcounts": [],  # TODO: to be implemented
            "nominated_beatmapset_count": 0,
            "page": {
                "html": "",
                "raw": "",
            },
            "pending_beatmapset_count": 0,
            "previous_usernames": [],
            "rank_highest": {
                "rank": 1,
                "updated_at": "2000-01-01T00:00:00+00:00",  # TODO: use datetime
            },
            "ranked_beatmapset_count": 0,
            "replays_watched_counts": [],
            "scores_best_count": 0,
            "scores_first_count": 0,
            "scores_pinned_count": 0,
            "scores_recent_count": 0,
            "statistics": {
                "count_100": 0,
                "count_300": 0,
                "count_50": 0,
                "count_miss": 0,
                "level": {
                    "current": utils.get_level(_user_stats["tscore"]),
                    "progress": 0,  # TODO: modify get_level() to include this
                },
                "global_rank": global_rank + 1,
                "global_rank_exp": None,
                "pp": _user_stats["pp"],
                "pp_exp": None,
                "ranked_score": _user_stats["rscore"],
                "hit_accuracy": _user_stats["acc"],
                "play_count": _user_stats["plays"],
                "play_time": _user_stats["playtime"],
                "total_score": _user_stats["tscore"],
                "total_hits": 0,  # TODO: to be implemented
                "maximum_combo": _user_stats["max_combo"],
                "replays_watched_by_others": 0,  # TODO: to be implemented
                "is_ranked": True,
                "grade_counts": {
                    "ss": _user_stats["x_count"],
                    "ssh": _user_stats["xh_count"],
                    "s": _user_stats["s_count"],
                    "sh": _user_stats["sh_count"],
                    "a": _user_stats["a_count"],
                },
                "country_rank": country_rank + 1,
                "rank": {
                    "country": country_rank + 1,
                },
            },
            "support_level": 0,
            "team": {"flag_url": "", "id": 1, "name": "Test", "short_name": "Test"},
            "user_achievements": [],
            "rank_history": {
                "mode": mode,
                "data": [],
            },
            "ranked_and_approved_beatmapset_count": 0,
            "unranked_beatmapset_count": 0,
        },
    )


@router.get("/api/v2/users/{user}/scores/{type}")
async def fetch_user_scores(
    user: int,
    type: Literal[
        "best",
        "recent",
        "firsts",  # TODO: to be implemented, not currently supported unless we made a big query i think, it's better to create a new table for this
    ],
    legacy_only: bool = Query(
        default=False,
        description="Whether or not to exclude lazer scores.",
    ),  # unused
    include_fails: str = Query(
        default="0",
        description="Only for recent scores, include scores of failed plays.",
    ),
    mode: Literal["osu", "taiko", "fruits", "mania"] = Query(
        default="osu",
        description="Ruleset of the scores to be returned.",
    ),
    limit: int = Query(
        default=100,
        description="Maximum number of results.",
    ),
    offset: str = Query(
        default="0",
        description="Result offset for pagination.",
    ),
) -> Score | dict[str, str] | list[dict[Any, Any]]:
    """
    This endpoint returns the scores of specified user.

    Parameters:
        user (int): id of the user.
        type (str): Score type. Must be one of these:
            - best = best scores
            - recent = recent scores
            - firsts = first scores

    Query parameters:
        legacy_only (int, optional): Whether or not to exclude lazer scores. Defaults to 0.
        include_fails (string, optional): Only for recent scores, include scores of failed plays. Set to 1 to include them. Defaults to 0.
        mode (str, optional): 'Ruleset' of the scores to be returned. Defaults to the specified user's mode.
            Valid values are:
            - osu = osu!standard
            - taiko = osu!taiko
            - fruits = osu!catch
            - mania = osu!mania
        limit (int, optional): Maximum number of results.
        offset (str, optional): Result offset for pagination.

    More info: https://osu.ppy.sh/docs/index.html#get-user-scores
    """
    _user = await users.fetch_by_user_id(id=user)

    if isinstance(_user, ServiceError):
        return {"error": ""}

    type_params: dict[Literal["best", "recent", "firsts"], Any] = {
        "best": {
            "sort_by": "pp",
            "score_statuses": [SubmissionStatus.BEST],
            "map_statuses": [RankedStatus.Ranked, RankedStatus.Approved],
        },
        "recent": {
            "sort_by": "play_time",
            "score_statuses": [
                SubmissionStatus.SUBMITTED,
                SubmissionStatus.BEST,
                (
                    SubmissionStatus.FAILED
                    if include_fails == "1"
                    else SubmissionStatus.SUBMITTED
                ),
                SubmissionStatus.BEST,
            ],
            "map_statuses": [RankedStatus.Ranked, RankedStatus.Approved],
        },
        # TODO: to be implemented
        "firsts": {
            "sort_by": "",
            "score_statuses": "",
            "map_statuses": "",
        },
    }

    _scores = await scores.fetch_many(
        user_id=_user["id"],
        mode=GameMode.from_string(mode),
        sort_by=type_params[type]["sort_by"],
        score_statuses=type_params[type]["score_statuses"],
        map_statuses=type_params[type]["map_statuses"],
        page=int(offset) + 1,
        page_size=limit,
    )

    if isinstance(_scores, ServiceError):
        return []

    validated_scores = [
        Score.model_validate(
            {
                "beatmap_id": score["beatmap_id"],
                "accuracy": score["acc"] / 100,
                "classic_total_score": score["score"],
                "best_id": score["id"],
                "ended_at": score["play_time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "id": score["id"],
                "max_combo": score["max_combo"],
                "mode": repr(GameMode(score["mode"])),
                "ruleset_id": repr(GameMode(score["mode"])),
                "mode_int": score["mode"],
                "mods": Mods.to_array(score["mods"]),
                "passed": False if score["status"] == SubmissionStatus.FAILED else True,
                "perfect": bool(score["perfect"]),
                "pp": score["pp"],
                "rank": score["grade"],
                "replay": False,  # TODO: add .env with BANCHO_PY_PATH to search for replays
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
                "daily_challenge_user_stats": {
                    "daily_streak_best": 0,
                    "daily_streak_current": 0,
                    "last_update": datetime(
                        2000,
                        1,
                        1,
                        0,
                        0,
                        0,
                    ),  # TODO: this is returning 2000-01-01T00:00:00Z but it should be 2000-01-01T00:00:00+00:00
                    "last_weekly_streak": datetime(
                        2000,
                        1,
                        1,
                        0,
                        0,
                        0,
                    ),  # TODO: this is returning 2000-01-01T00:00:00Z but it should be 2000-01-01T00:00:00+00:00
                    "playcount": 0,
                    "top_10p_placements": 0,
                    "top_50p_placements": 0,
                    "user_id": _user["id"],
                    "weekly_streak_best": 0,
                    "weekly_streak_current": 0,
                },
            },
        )
        for score in _scores
    ]

    return [score.model_dump() for score in validated_scores]
