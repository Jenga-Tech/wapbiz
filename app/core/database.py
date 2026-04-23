from collections.abc import AsyncGenerator

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


def get_sync_database_url() -> str:
    """
    Alembic runs with a synchronous engine.
    Convert SQLAlchemy async URLs like `postgresql+psycopg://...`
    to a sync-compatible psycopg URL for migrations.
    """
    url = make_url(settings.database_url)

    if url.drivername == "postgresql+psycopg":
        return str(url.set(drivername="postgresql+psycopg"))

    return settings.database_url


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session