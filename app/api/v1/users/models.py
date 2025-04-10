from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    join_date: str
    count300: int
    count100: int
    count50: int
    playcount: int
    ranked_score: int
    total_score: int
    pp_rank: int
    level: int
    pp_raw: int
    accuracy: float
    count_rank_ss: int
    count_rank_ssh: int
    count_rank_s: int
    count_rank_sh: int
    count_rank_a: int
    country: str
    total_seconds_played: int
    pp_country_rank: int
    events: list[Any]
