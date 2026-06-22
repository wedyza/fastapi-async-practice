import asyncio
from typing import Any


async def asleep(ctx: dict[str, Any], seconds: int = 5) -> None:
    await asyncio.sleep(seconds)
