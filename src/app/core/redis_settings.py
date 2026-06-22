from arq.connections import ArqRedis, RedisSettings, create_pool

from src.app.core.config import settings

redis_settings = RedisSettings(
        settings.REDIS_SETTINGS.REDIS_HOST,
        settings.REDIS_SETTINGS.REDIS_PORT,
        database=settings.REDIS_SETTINGS.REDIS_DB
    )

_worker_client: ArqRedis | None = None

async def get_worker_client() -> ArqRedis:
    if _worker_client is None:
        raise RuntimeError("ArqRedis client not initialized")
    return _worker_client

async def init_worker_client():
    global _worker_client
    _worker_client = await create_pool(redis_settings)

async def close_worker_client():
    global _worker_client
    if _worker_client:
        await _worker_client.close()
        _worker_client = None
