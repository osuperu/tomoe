from __future__ import annotations

from typing import TypedDict
from typing import cast

from common import clients

READ_PARAMS = """
    id,
    name,
    safe_name,
    email,
    priv,
    pw_bcrypt,
    country,
    silence_end,
    donor_end,
    creation_time,
    latest_activity,
    clan_id,
    clan_priv,
    preferred_mode,
    play_style,
    custom_badge_name,
    custom_badge_icon,
    userpage_content,
    api_key
"""


class User(TypedDict):
    id: int
    name: str
    safe_name: str
    email: str
    priv: int
    pw_bcrypt: str
    country: str
    silence_end: int
    donor_end: int
    creation_time: int
    latest_activity: int
    clan_id: int
    clan_priv: int
    preferred_mode: int
    play_style: int
    custom_badge_name: str
    custom_badge_icon: str
    userpage_content: str
    api_key: str
    online: bool


async def fetch_by_user_id(id: int) -> User | None:
    """
    Fetch a user by user ID.

    Args:
        id (int): The ID of the user to fetch.

    Returns:
        User | None: The user object if found, None otherwise.
    """
    user = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM users
            WHERE id = :id
        """,
        values={
            "id": id,
        },
    )
    return cast(User, user) if user is not None else None


async def fetch_by_username(username: str) -> User | None:
    """
    Fetch a user by username.

    Args:
        username (str): The username of the user to fetch.

    Returns:
        User | None: The user object if found, None otherwise.
    """
    user = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM users
            WHERE name = :username OR safe_name = :safe_name
        """,
        values={
            "username": username,
            "safe_name": username.lower(),
        },
    )
    return cast(User, user) if user is not None else None
