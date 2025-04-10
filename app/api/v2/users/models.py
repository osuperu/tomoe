from __future__ import annotations

from datetime import datetime
from enum import Enum
from enum import unique
from typing import Literal

from pydantic import BaseModel
from pydantic import Field


class UserKudosu(BaseModel):
    total: int
    available: int


class Country(BaseModel):
    code: str
    name: str


class UserProfileCover(BaseModel):
    url: str
    custom_url: str | None = None
    id: str | None = None


UserAccountHistoryType = Literal[
    "note",
    "restriction",
    "silence",
    "tournament_ban",
]

Gamemode = Literal[
    "osu",
    "taiko",
    "fruits",
    "mania",
]


class UserAccountHistory(BaseModel):
    id: int
    timestamp: datetime
    length: int
    permanent: bool
    type: UserAccountHistoryType
    description: str | None = None


class UserProfileTournamentBanner(BaseModel):
    tournament_id: int
    id: int | None = None
    image: str | None = None
    image_2_x: str | None = Field(default=None, alias="image@2x")


class UserBadge(BaseModel):
    awarded_at: datetime
    description: str
    image_url: str
    image_2x_url: str = Field(alias="image@2x_url")
    url: str


class UserRelation(BaseModel):
    target_id: int
    relation_type: str
    mutual: bool
    target: User | None = None


class UserGroup(BaseModel):
    id: int
    identifier: str
    name: str
    short_name: str
    has_listing: bool
    has_playmodes: bool
    is_probationary: bool
    colour: str | None = None
    playmodes: list[Gamemode] | None = None
    description: str | None = None


class TimestampedCount(BaseModel):
    start_date: datetime
    count: int


class HTMLBody(BaseModel):
    html: str
    raw: str | None = None
    bbcode: str | None = None


class UserRankHighest(BaseModel):
    rank: int
    updated_at: datetime


class UserRankHistoryElement(BaseModel):
    mode: str
    data: list[int]


class UserGradeCounts(BaseModel):
    ssh: int
    ss: int
    sh: int
    s: int
    a: int


class UserLevel(BaseModel):
    current: int
    progress: int


class UserStats(BaseModel):
    """Fields are marked as optional since they might be missing from rankings other than performance."""

    ranked_score: int | None = None
    play_count: int | None = None
    grade_counts: UserGradeCounts | None = None
    total_hits: int | None = None
    is_ranked: bool | None = None
    total_score: int | None = None
    level: UserLevel | None = None
    hit_accuracy: float | None = None
    play_time: int | None = None
    pp: float | None = None
    pp_exp: float | None = None
    replays_watched_by_others: int | None = None
    maximum_combo: int | None = None
    global_rank: int | None = None
    global_rank_exp: int | None = None
    country_rank: int | None = None
    user: User | None = None
    count_300: int | None = None
    count_100: int | None = None
    count_50: int | None = None
    count_miss: int | None = None
    variants: list[UserStatsVariant] | None = None


class UserStatsVariant(BaseModel):
    mode: Gamemode
    variant: str
    pp: float
    country_rank: int | None = None
    global_rank: int | None = None


class UserStatsRulesets(BaseModel):
    osu: UserStats | None = None
    taiko: UserStats | None = None
    fruits: UserStats | None = None
    mania: UserStats | None = None


class UserAchievmement(BaseModel):
    achieved_at: datetime
    achievement_id: int


class UserTeam(BaseModel):
    flag_url: str
    id: int
    name: str
    short_name: str


class DailyChallengeUserStats(BaseModel):
    daily_streak_best: int
    daily_streak_current: int
    last_update: datetime
    last_weekly_streak: datetime
    playcount: int
    top_10p_placements: int
    top_50p_placements: int
    user_id: int
    weekly_streak_best: int
    weekly_streak_current: int


class User(BaseModel):
    avatar_url: str
    country_code: str
    id: int
    username: str
    cover_url: str | None = None
    default_group: str | None = None
    is_active: bool | None = None
    is_bot: bool | None = None
    is_online: bool | None = None
    is_supporter: bool | None = None
    pm_friends_only: bool | None = None
    profile_colour: str | None = None
    is_deleted: bool | None = None
    last_visit: datetime | None = None
    discord: str | None = None
    has_supported: bool | None = None
    interests: str | None = None
    join_date: datetime | None = None
    kudosu: UserKudosu | None = None
    location: str | None = None
    max_blocks: int | None = None
    max_friends: int | None = None
    occupation: str | None = None
    playmode: Gamemode | None = None
    playstyle: list[str] | None = None
    post_count: int | None = None
    profile_hue: int | None = None
    profile_order: list[str] | None = None
    title: str | None = None
    twitter: str | None = None
    website: str | None = None
    country: Country | None = None
    cover: UserProfileCover | None = None
    is_restricted: bool | None = None
    account_history: list[UserAccountHistory] | None = None
    active_tournament_banner: UserProfileTournamentBanner | None = None
    active_tournament_banners: list[UserProfileTournamentBanner] | None = None
    badges: list[UserBadge] | None = None
    daily_challenge_user_stats: DailyChallengeUserStats | None = None
    beatmap_playcounts_count: int | None = None
    favourite_beatmapset_count: int | None = None
    comments_count: int | None = None
    follow_user_mapping: list[int] | None = None
    follower_count: int | None = None
    friends: list[UserRelation] | None = None
    graveyard_beatmapset_count: int | None = None
    groups: list[UserGroup] | None = None
    loved_beatmapset_count: int | None = None
    mapping_follower_count: int | None = None
    monthly_playcounts: list[TimestampedCount] | None = None
    page: HTMLBody | None = None
    pending_beatmapset_count: int | None = None
    previous_usernames: list[str] | None = None
    rank_highest: UserRankHighest | None = None
    rank_history: UserRankHistoryElement | None = None
    ranked_beatmapset_count: int | None = None
    replays_watched_counts: list[TimestampedCount] | None = None
    scores_best_count: int | None = None
    scores_first_count: int | None = None
    scores_recent_count: int | None = None
    statistics: UserStats | None = None
    statistics_rulesets: UserStatsRulesets | None = None
    support_level: int | None = None
    team: UserTeam | None = None
    unread_pm_count: int | None = None
    user_achievements: list[UserAchievmement] | None = None
