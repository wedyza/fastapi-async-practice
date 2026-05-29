from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.infrastructure.postgresql.db_config import settings

async_engine = create_async_engine(
    settings.database_url_asyncpg, echo=True, pool_size=5, pool_pre_ping=True
)

async_session_factory = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, autoflush=False
)
