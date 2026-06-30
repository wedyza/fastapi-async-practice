import json
from asyncio import TaskGroup
from typing import Any

from httpx import AsyncClient

from redis.asyncio import Redis


async def fetch_url(client: AsyncClient, url: str) -> dict[Any, Any]:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()

async def fetch(ctx: dict[str, Any], urls: list[str]):
    client: AsyncClient = ctx['session']
    redis_client: Redis = ctx['redis_client']
    tasks: list[Any] = []
    async with TaskGroup() as tg:
        for url in urls:
            tasks.append(tg.create_task(fetch_url(client, url)))  # noqa: PERF401
    results: list[dict[str, str]] = [task.result() for task in tasks]
    await redis_client.set(f'fetch:{ctx['job_id']}', json.dumps(results), 15 * 60)
    return tasks
