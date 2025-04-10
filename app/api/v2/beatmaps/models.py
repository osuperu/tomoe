from __future__ import annotations

from datetime import datetime
from enum import Enum
from enum import unique
from typing import Any
from typing import Literal

from api.v2.users.models import Gamemode
from api.v2.users.models import User
from pydantic import BaseModel
from pydantic import Field


class ScoreStatistics(BaseModel):
    count_miss: int
    count_50: int
    count_100: int
    count_300: int
    count_geki: int
    count_katu: int
    count_large_tick_miss: int | None = None
    count_slider_tail_hit: int | None = None


ScoreType = Literal[
    "solo_score",
    "score_best_osu",
    "score_best_taiko",
    "score_best_fruits",
    "score_best_mania",
    "score_osu",
    "score_taiko",
    "score_fruits",
    "score_mania",
    "legacy_match_score",
]


BeatmapRankStatus = Literal[
    "graveyard",
    "wip",
    "pending",
    "ranked",
    "approved",
    "qualified",
    "loved",
]

Mod = Literal[
    "NM",
    "NF",
    "EZ",
    "TD",
    "HD",
    "HR",
    "SD",
    "DT",
    "RX",
    "HT",
    "NC",
    "FL",
    "AT",
    "SO",
    "AP",
    "PF",
    "4K",
    "5K",
    "6K",
    "7K",
    "8K",
    "FI",
    "RD",
    "CN",
    "TP",
    "9K",
    "CO",
    "1K",
    "3K",
    "2K",
    "V2",
    "MR",
]


class BeatmapFailtimes(BaseModel):
    exit: list[int] | None = None
    fail: list[int] | None = None


class Beatmap(BaseModel):
    id: int
    url: str
    mode: Gamemode
    beatmapset_id: int
    difficulty_rating: float
    status: BeatmapRankStatus
    total_length: int
    user_id: int
    version: str
    accuracy: float | None = None
    ar: float | None = None
    cs: float | None = None
    bpm: float | None = None
    convert: bool | None = None
    count_circles: int | None = None
    count_sliders: int | None = None
    count_spinners: int | None = None
    deleted_at: datetime | None = None
    drain: float | None = None
    hit_length: int | None = None
    is_scoreable: bool | None = None
    last_updated: datetime | None = None
    passcount: int | None = None
    playcount: int | None = None
    checksum: str | None = None
    max_combo: int | None = None
    beatmapset: Beatmapset | None = None
    failtimes: BeatmapFailtimes | None = None


class BeatmapCovers(BaseModel):
    cover: str
    card: str
    list: str
    slimcover: str
    cover_2_x: str | None = Field(default=None, alias="cover@2x")
    card_2_x: str | None = Field(default=None, alias="card@2x")
    list_2_x: str | None = Field(default=None, alias="list@2x")
    slimcover_2_x: str | None = Field(default=None, alias="slimcover@2x")


class BeatmapHype(BaseModel):
    current: int
    required: int


class BeatmapAvailability(BaseModel):
    more_information: str | None = None
    download_disabled: bool | None = None


class BeatmapNominations(BaseModel):
    current: int | None = None
    required: int | None = None


class BeatmapNomination(BaseModel):
    beatmapset_id: int
    reset: bool
    user_id: int
    rulesets: list[Gamemode] | None = None


class PinAttributes(BaseModel):
    is_pinned: bool
    score_id: int
    score_type: ScoreType | None = None


class CurrentUserAttributes(BaseModel):
    can_beatmap_update_owner: bool | None = None
    can_delete: bool | None = None
    can_edit_metadata: bool | None = None
    can_edit_tags: bool | None = None
    can_hype: bool | None = None
    can_hype_reason: str | None = None
    can_love: bool | None = None
    can_remove_from_loved: bool | None = None
    is_watching: bool | None = None
    new_hype_time: datetime | None = None
    nomination_modes: list[Gamemode] | None = None
    remaining_hype: int | None = None
    can_destroy: bool | None = None
    can_reopen: bool | None = None
    can_moderate_kudosu: bool | None = None
    can_resolve: bool | None = None
    vote_score: int | None = None
    can_message: bool | None = None
    can_message_error: str | None = None
    last_read_id: int | None = None
    can_new_comment: bool | None = None
    can_new_comment_reason: str | None = None
    pin: PinAttributes | None = None


class BeatmapDescription(BaseModel):
    bbcode: str | None = None
    description: str | None = None


class BeatmapGenre(BaseModel):
    name: str
    id: int | None = None


class BeatmapLanguage(BaseModel):
    name: str
    id: int | None = None


BeatmapsetDisscussionType = Literal[
    "hype",
    "praise",
    "problem",
    "review",
    "suggestion",
    "mapper_note",
]


class BeatmapsetDiscussion(BaseModel):
    id: int
    beatmapset_id: int
    user_id: int
    message_type: BeatmapsetDisscussionType
    resolved: bool
    can_be_resolved: bool
    can_grant_kudosu: bool
    created_at: datetime
    beatmap_id: int | None = None
    deleted_by_id: int | None = None
    parent_id: int | None = None
    timestamp: int | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    last_post_at: datetime | None = None
    kudosu_denied: bool | None = None
    starting_post: BeatmapsetDiscussionPost | None = None


class BeatmapsetDiscussionPost(BaseModel):
    id: int
    user_id: int
    system: bool
    message: str
    created_at: datetime
    beatmap_discussion_id: int | None = None
    last_editor_id: int | None = None
    deleted_by_id: int | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


BeatmapsetEventType = Literal[
    "approve",
    "beatmap_owner_change",
    "discussion_delete",
    "discussion_post_delete",
    "discussion_post_restore",
    "discussion_restore",
    "discussion_lock",
    "discussion_unlock",
    "disqualify",
    "genre_edit",
    "issue_reopen",
    "issue_resolve",
    "kudosu_allow",
    "kudosu_deny",
    "kudosu_gain",
    "kudosu_lost",
    "kudosu_recalculate",
    "language_edit",
    "love",
    "nominate",
    "nomination_reset",
    "nomination_reset_received",
    "nsfw_toggle",
    "offset_edit",
    "qualify",
    "rank",
    "remove_from_loved",
]


class BeatmapsetEvent(BaseModel):
    id: int
    type: BeatmapsetEventType
    created_at: datetime
    user_id: int | None = None
    beatmapset: Beatmapset | None = None
    discussion: BeatmapsetDiscussion | None = None
    comment: dict[Any, Any] | None = None


class BeatmapNominationsSummary(BaseModel):
    current: int
    required_meta: BeatmapNominationsRequired
    eligible_main_rulesets: list[Gamemode] | None = None


class BeatmapNominationsRequired(BaseModel):
    main_ruleset: int
    non_main_ruleset: int


class Beatmapset(BaseModel):
    id: int
    artist: str
    artist_unicode: str
    covers: BeatmapCovers
    creator: str
    favourite_count: int
    play_count: int | None = None
    preview_url: str
    source: str
    status: BeatmapRankStatus
    title: str
    title_unicode: str
    user_id: int
    video: bool
    nsfw: bool | None = None
    hype: BeatmapHype | None = None
    availability: BeatmapAvailability | None = None
    bpm: float | None = None
    can_be_hyped: bool | None = None
    discussion_enabled: bool | None = None
    discussion_locked: bool | None = None
    is_scoreable: bool | None = None
    last_updated: datetime | None = None
    nominations_summary: BeatmapNominationsSummary | None = None
    legacy_thread_url: str | None = None
    nominations: BeatmapNominations | None = None
    current_nominations: list[BeatmapNomination] | None = None
    ranked_date: datetime | None = None
    storyboard: bool | None = None
    submitted_date: datetime | None = None
    tags: str | None = None
    pack_tags: list[str] | None = None
    track_id: int | None = None
    user: User | None = None
    related_users: list[User] | None = None
    current_user_attributes: CurrentUserAttributes | None = None
    description: BeatmapDescription | None = None
    genre: BeatmapGenre | None = None
    language: BeatmapLanguage | None = None
    ratings: list[int] | None = None
    recent_favourites: list[User] | None = None
    discussions: list[BeatmapsetDiscussion] | None = None
    events: list[BeatmapsetEvent] | None = None
    has_favourited: bool | None = None
    beatmaps: list[Beatmap] | None = None
    converts: list[Beatmap] | None = None


class ScoreWeight(BaseModel):
    percentage: float
    pp: float


class Score(BaseModel):
    id: int | None = None
    best_id: int | None = None
    user_id: int
    accuracy: float
    max_combo: int
    statistics: ScoreStatistics
    pp: float | None = 0
    rank: str
    passed: bool
    current_user_attributes: CurrentUserAttributes | None = None
    classic_total_score: int | None = None
    processed: bool | None = None
    replay: bool
    maximum_statistics: ScoreStatistics | None = None
    mods: list[Mod]
    ruleset_id: Gamemode
    started_at: datetime | None = None
    ended_at: datetime | None = None
    ranked: bool | None = None
    preserve: bool | None = None
    beatmap_id: int | None = None
    build_id: int | None = None
    has_replay: bool | None = None
    is_perfect_combo: bool | None = None
    total_score: int | None = None
    total_score_without_mods: int | None = None
    perfect: bool
    mode: Gamemode
    type: ScoreType
    beatmap: Beatmap | None = None
    beatmapset: Beatmapset | None = None
    weight: ScoreWeight | None = None
    user: User | None = None


class BeatmapScore(BaseModel):
    score_count: int
    scores: list[Score]
