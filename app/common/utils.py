from __future__ import annotations

from enum import IntEnum
from enum import unique

BPY_RANKED_STATUS = {
    "pending": 0,
    "ranked": 2,
    "approved": 3,
    "qualified": 4,
    "loved": 5,
}

BPY_RANKED_STATUS_REPR_LIST = (
    "pending",
    "",
    "ranked",
    "approved",
    "qualified",
)

GAMEMODE_REPR_LIST = (
    "osu",
    "taiko",
    "fruits",
    "mania",
)


@unique
class GameMode(IntEnum):
    OSU = 0
    TAIKO = 1
    FRUITS = 2
    MANIA = 3

    def __repr__(self) -> str:
        return GAMEMODE_REPR_LIST[self.value]

    @classmethod
    def from_string(cls, mode: str) -> int:
        return GAMEMODE_REPR_LIST.index(mode) if mode in GAMEMODE_REPR_LIST else 0


@unique
class RankedStatus(IntEnum):
    NotSubmitted = -1
    Pending = 0
    UpdateAvailable = 1
    Ranked = 2
    Approved = 3
    Qualified = 4
    Loved = 5

    def __repr__(self) -> str:
        return BPY_RANKED_STATUS_REPR_LIST[self.value]


@unique
class SubmissionStatus(IntEnum):
    FAILED = 0
    SUBMITTED = 1
    BEST = 2


def get_required_score_for_level(level: int) -> float:
    if level <= 100:
        if level >= 2:
            return 5000 / 3 * (4 * (level**3) - 3 * (level**2) - level) + 1.25 * (
                1.8 ** (level - 60)
            )
        else:
            return 1.0  # Should be 0, but we get division by 0 below so set to 1
    else:
        return 26931190829 + 1e11 * (level - 100)


def get_level(totalScore: int) -> int:
    level = 1
    while True:
        # Avoid endless loops
        if level > 120:
            return level

        # Calculate required score
        reqScore = get_required_score_for_level(level)

        # Check if this is our level
        if totalScore <= reqScore:
            # Our level, return it and break
            return level - 1
        else:
            # Not our level, calculate score for next level
            level += 1
