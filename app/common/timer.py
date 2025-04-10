from __future__ import annotations

import time
from types import TracebackType


class Timer:
    def __init__(self) -> None:
        self.start_time: float | None = None
        self.end_time: float | None = None

    async def __aenter__(self) -> Timer:
        self.start_time = time.time()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.end_time = time.time()

    def elapsed(self) -> float:
        if self.start_time is None or self.end_time is None:
            raise ValueError("Timer has not been started or stopped.")
        return self.end_time - self.start_time
