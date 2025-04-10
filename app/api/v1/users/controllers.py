from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import Any

from api.v1.users.models import User
from common import clients
from common import utils
from errors import ServiceError
from fastapi import APIRouter
from fastapi import Query
from services import stats
from services import users

router = APIRouter()


@router.get("/api/get_user")
async def get_user(
    k: str,
    u: str,
    m: int = Query(
        default=0,
        description="Gamemode integer (0 = osu!, 1 = osu!taiko, 2 = osu!catch, 3 = osu!mania)",
    ),
    type: str | None = Query(
        default=None,
        description="Specify if 'u' is a User ID ('id') or a username ('string')",
    ),
    event_days: int = Query(
        default=1,
        description="Max number of days between now and last event date (1-31)",
    ),  # TODO: unused for now
) -> User | dict[str, str]:
    """
    Query parameters:
    - k (str): API Key (Required).
    - u (str): User ID or username (Required).
    - m (int, optional): Gamemode integer. Defaults to 0.
      - 0 = osu!
      - 1 = osu!taiko
      - 2 = osu!catch
      - 3 = osu!mania
    - type (str, optional): Specifies if 'u' is a User ID or a username.
      - "string" for usernames
      - "id" for user IDs
      - Defaults to automatic recognition.
    - event_days (int, optional): Max number of days between now and the last event date.
      - Range: 1-31
      - Defaults to 1.

    More info: https://github.com/ppy/osu-api/wiki#apiget_user
    """
    is_user_id = type == "u" or (isinstance(u, str) and u.isdigit())

    if is_user_id:
        user = await users.fetch_by_user_id(id=int(u))
    else:
        user = await users.fetch_by_username(username=u)

    if isinstance(user, ServiceError):
        return {}

    user_stats = await stats.fetch_one(user_id=user["id"], mode=m)
    # TODO: fix crash when the user never played in the specified mode
    global_rank = await clients.redis.zrevrank(
        f"bancho:leaderboard:{m}",
        user["id"],
    )
    country_rank = await clients.redis.zrevrank(
        f"bancho:leaderboard:{m}:{user['country']}",
        user["id"],
    )

    if isinstance(user_stats, ServiceError):
        return {}

    return User.model_validate(
        {
            "user_id": user["id"],
            "username": user["name"],
            "join_date": datetime.fromtimestamp(
                user["creation_time"],
                tz=timezone.utc,
            ).strftime(
                "%Y-%m-%d %H:%M:%S",
            ),  # TODO: check if this is correct
            "count300": 0,
            "count100": 0,
            "count50": 0,
            "playcount": user_stats["plays"],
            "ranked_score": user_stats["rscore"],
            "total_score": user_stats["tscore"],
            "pp_rank": global_rank + 1,
            "level": utils.get_level(user_stats["tscore"]),
            "pp_raw": user_stats["pp"],
            "accuracy": user_stats["acc"],
            "count_rank_ss": user_stats["x_count"],
            "count_rank_ssh": user_stats["xh_count"],
            "count_rank_s": user_stats["s_count"],
            "count_rank_sh": user_stats["sh_count"],
            "count_rank_a": user_stats["a_count"],
            "country": user["country"].upper(),
            "total_seconds_played": user_stats["playtime"],
            "pp_country_rank": country_rank + 1,
            "events": [],  # TODO: to be implemented
        },
    )
