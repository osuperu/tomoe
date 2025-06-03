from __future__ import annotations

from fastapi import APIRouter

rest_api_router = APIRouter()

from api.v1.osu.controllers import router as v1_osu_router
from api.v1.users.controllers import router as v1_accounts_router
from api.v2.beatmaps.controllers import router as v2_beatmaps_router
from api.v2.beatmapsets.controller import router as v2_beatmapsets_router
from api.v2.scores.controllers import router as v2_scores_router
from api.v2.users.controllers import router as v2_accounts_router

rest_api_router.include_router(v1_osu_router)
rest_api_router.include_router(v1_accounts_router)
rest_api_router.include_router(v2_beatmaps_router)
rest_api_router.include_router(v2_scores_router)
rest_api_router.include_router(v2_accounts_router)
rest_api_router.include_router(v2_beatmapsets_router)
