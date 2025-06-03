from __future__ import annotations

from common import storage
from common.utils import BPY_INITIAL_MAP_ID
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.responses import Response

router = APIRouter()


@router.get("/osu/{map_id}")
async def get_osu_file(map_id: str) -> Response:
    """
    Handle a osu download request.
    """
    if int(map_id) >= BPY_INITIAL_MAP_ID:
        osu_disk_file = storage.get_beatmap_file(int(map_id))

        return Response(
            content=osu_disk_file,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{map_id}.osu"',
            },
        )

    return RedirectResponse(
        url=f"https://osu.ppy.sh/osu/{map_id}",
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
