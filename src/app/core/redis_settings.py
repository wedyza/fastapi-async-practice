from arq.connections import ArqRedis, RedisSettings, create_pool

from redis.asyncio import Redis
from src.app.core.config import settings

redis_settings = RedisSettings(
        settings.REDIS_SETTINGS.REDIS_HOST,
        settings.REDIS_SETTINGS.REDIS_PORT,
        database=settings.REDIS_SETTINGS.REDIS_DB
    )

_worker_client: ArqRedis | None = None

_redis_client: Redis | None = None

NON_TARGET_JOBS = ["send_email_with_otp"]

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

async def get_redis_client() -> Redis:
    if _redis_client is None:
        raise RuntimeError("Redis client is not initialized")
    return _redis_client

async def init_redis_client():
    global _redis_client
    _redis_client = Redis(
        host=settings.REDIS_SETTINGS.REDIS_HOST,
        port=settings.REDIS_SETTINGS.REDIS_PORT,
        db=settings.REDIS_SETTINGS.REDIS_DB,
        decode_responses=True
    )

async def close_redis_client():
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None

async def enqueue_job(job_type: str, job_id: str = "", *args, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    redis = await get_worker_client()
    try:
        if job_type in NON_TARGET_JOBS:
            await redis.enqueue_job(job_type, *args, **kwargs)  # pyright: ignore[reportUnknownArgumentType]
        else:
            await redis.enqueue_job(job_type, *args, **kwargs, _job_id=job_id, _queue_name='ЭЩКЕРЕЕЕ')  # pyright: ignore[reportUnknownArgumentType]
    except Exception as _:
        ...
