from __future__ import annotations

from pyexpat import model
from typing import Any

from api.v2.beatmaps.models import Beatmapset
from api.v2.users.models import User
from common import settings
from common import utils
from common.utils import GameMode
from common.utils import RankedStatus
from errors import ServiceError
from fastapi import APIRouter
from fastapi import Query
from services import maps

router = APIRouter()


@router.get("/api/v2/beatmapsets/lookup")
async def fetch_beatmapset(
    beatmap_id: int = Query(
        description="Beatmap ID to look up.",
    ),
) -> Any:
    _map = await maps.fetch_one(id=beatmap_id)

    if isinstance(_map, ServiceError):
        return {
            "error": "Specified beatmap difficulty couldn't be found.",
        }

    _maps = await maps.fetch_many(set_id=_map["set_id"])

    if isinstance(_maps, ServiceError):
        return {}

    return Beatmapset.model_validate(
        {
            "id": _maps[0]["set_id"],
            "artist": _maps[0]["artist"],
            "artist_unicode": _maps[0]["artist"],
            "covers": {
                "cover": f"https://assets.ppy.sh/beatmaps/{_maps[0]['set_id']}/covers/cover.jpg",
                "cover@2x": f"https://assets.ppy.sh/beatmaps/{_maps[0]['set_id']}/covers/cover@2x.jpg",
                "card": f"https://assets.ppy.sh/beatmaps/{_maps[0]['set_id']}/covers/card.jpg",
                "card@2x": f"https://assets.ppy.sh/beatmaps/{_maps[0]['set_id']}/covers/card@2x.jpg",
                "list": f"{settings.BANCHOPY_MAPS_BASE_URL}/thumb/{_maps[0]['set_id']}l.jpg",
                "list@2x": f"{settings.BANCHOPY_MAPS_BASE_URL}/thumb/{_maps[0]['set_id']}l.jpg",
                "slimcover": f"https://assets.ppy.sh/beatmaps/{_maps[0]['set_id']}/covers/slimcover.jpg",
                "slimcover@2x": f"https://assets.ppy.sh/beatmaps/{_maps[0]['set_id']}/covers/slimcover@2x.jpg",
            },
            "creator": _maps[0]["creator"],
            "favourite_count": 0,  # TODO: to be implemented, add favourites service
            "play_count": _maps[0]["plays"],
            "preview_url": f"https://b.ppy.sh/preview/{_maps[0]['set_id']}.mp3",
            "source": "",  # TODO: maybe make an api call to get this?
            "status": repr(RankedStatus(_maps[0]["status"])),
            "title": _maps[0]["title"],
            "title_unicode": _maps[0]["title"],
            "user_id": 3,  # TODO. placeholder, should be the user id of the creator but idk how to handle it
            "video": False,  # TODO: maybe make an api call to get this?
            "nsfw": False,  # TODO: maybe make an api call to get this?
            "availability": {
                "more_information": None,
                "download_disabled": False,
            },
            "can_be_hyped": False,
            "discussion_enabled": True,
            "discussion_locked": False,
            "is_scoreable": True,
            "last_updated": _maps[0]["last_update"].strftime("%Y-%m-%dT%H:%M:%SZ"),
            "nominations_summary": {
                "current": 2,  # placeholder, idk if add this field to the db or make an api call to get this
                "eligible_main_rulesets": [
                    "osu",  # TODO: add a loop to get this
                ],
                "required_meta": {
                    "main_ruleset": 0,
                    "non_main_ruleset": 0,
                },
            },
            "storyboard": False,  # TODO: maybe make an api call to get this?
            "tags": "",  # TODO: maybe make an api call to get this?
            "genre": {
                "id": 7,  # placeholder, idk if add this field to the db or make an api call to get this
                "name": "Novelty",  # placeholder, idk if add this field to the db or make an api call to get this
            },
            "language": {
                "id": 3,  # placeholder, idk if add this field to the db or make an api call to get this
                "name": "Japanese",  # placeholder, idk if add this field to the db or make an api call to get this
            },
            "beatmaps": [
                {
                    "id": map["id"],
                    "url": f"https://{settings.DOMAIN}/b/{map['id']}",
                    "mode": repr(GameMode(map["mode"])),
                    "beatmapset_id": map["set_id"],
                    "difficulty_rating": map["diff"],
                    "status": repr(RankedStatus(map["status"])),
                    "total_length": map["total_length"],
                    "user_id": 3,  # TODO. placeholder, should be the user id of the creator but idk how to handle it
                    "version": map["version"],
                    "is_scoreable": True,
                    "last_updated": map["last_update"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "accuracy": map["od"],
                    "ar": map["ar"],
                    "bpm": map["bpm"],
                    "cs": map["cs"],
                    "drain": map["hp"],
                    "convert": False,  # maybe make an api call to get this?
                    "count_circles": 200,  # placeholder, idk if add this field to the db or make an api call to get this
                    "count_sliders": 0,  # placeholder, idk if add this field to the db or make an api call to get this
                    "count_spinners": 0,  # placeholder, idk if add this field to the db or make an api call to get this
                    "hit_length": map["total_length"],
                    "passcount": 0,  # placeholder, idk if add this field to the db or make an api call to get this
                    "playcount": map["plays"],
                }
                for map in _maps
            ],
            "converts": [  # TODO: this is a copypaste from beatmaps key
                {
                    "id": map["id"],
                    "url": f"https://{settings.DOMAIN}/b/{map['id']}",
                    "mode": repr(GameMode(map["mode"])),
                    "beatmapset_id": map["set_id"],
                    "difficulty_rating": map["diff"],
                    "status": repr(RankedStatus(map["status"])),
                    "total_length": map["total_length"],
                    "user_id": 3,  # TODO. placeholder, should be the user id of the creator but idk how to handle it
                    "version": map["version"],
                    "is_scoreable": True,
                    "last_updated": map["last_update"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "accuracy": map["od"],
                    "ar": map["ar"],
                    "bpm": map["bpm"],
                    "cs": map["cs"],
                    "drain": map["hp"],
                    "convert": False,  # maybe make an api call to get this?
                    "count_circles": 0,  # placeholder, idk if add this field to the db or make an api call to get this
                    "count_sliders": 0,  # placeholder, idk if add this field to the db or make an api call to get this
                    "count_spinners": 0,  # placeholder, idk if add this field to the db or make an api call to get this
                    "hit_length": map["total_length"],
                    "passcount": 0,  # placeholder, idk if add this field to the db or make an api call to get this
                    "playcount": map["plays"],
                }
                for map in _maps
            ],
            "user": User.model_validate(
                {
                    "avatar_url": "https://osu.ppy.sh/images/layout/avatar-guest@2x.png",
                    "country_code": "JP",
                    "default_group": "default",
                    "id": 1881639,
                    "is_active": True,
                    "is_bot": False,
                    "is_deleted": False,
                    "is_online": True,
                    "is_supporter": False,
                    "last_visit": "2025-04-07T23:23:57+00:00",
                    "pm_friends_only": False,
                    "profile_colour": None,
                    "username": _maps[0]["creator"],
                    "team": {
                        "flag_url": "",
                        "id": 1,
                        "name": "Test",
                        "short_name": "Test",
                    },
                },
            ),
        },
    )
