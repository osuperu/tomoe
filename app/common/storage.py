from __future__ import annotations

import os
from pathlib import Path

from common import logger
from common import settings

DATA_PATH = Path(settings.BANCHOPY_FOLDER) / ".data"


def get_file_content(filepath: str) -> bytes | None:
    try:
        with open(f"{DATA_PATH}/{filepath}", "rb") as f:
            return f.read()
    except Exception as e:
        logger.error(f'The file "{filepath}" doesn\'t exist')
        return None


def save_to_file(filepath: str, content: bytes) -> bool:
    try:
        with open(f"{DATA_PATH}/{filepath}", "wb") as f:
            f.write(content)
    except Exception as e:
        logger.error(f'Failed to save file "{filepath}": {e}')
        return False

    return True


def remove_file(filepath: str) -> bool:
    try:
        os.remove(f"{DATA_PATH}/{filepath}")
    except Exception as e:
        logger.error(f'Failed to file "{filepath}": "{e}"')
        return False

    return True


def file_exists(key: str, extension: str, bucket: str) -> bool:
    return os.path.isfile(f"{DATA_PATH}/{bucket}/{key}.{extension}")


def get(key: str, extension: str, bucket: str) -> bytes | None:
    return get_file_content(f"{bucket}/{key}.{extension}")


def get_beatmap_file(id: int) -> bytes | None:
    return get(str(id), "osu", "osu")
