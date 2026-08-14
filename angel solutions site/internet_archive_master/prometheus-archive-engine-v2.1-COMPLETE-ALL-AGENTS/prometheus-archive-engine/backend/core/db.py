"""
Prometheus Archive Engine - Database Core Connections
Supports PostgreSQL and local SQLite async connections
"""
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

# Retrieve database URL from environmental variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./prometheus.db")

# Connection pool tuning parameters based on database engine type
is_sqlite = DATABASE_URL.startswith("sqlite")

connect_args = {"check_same_thread": False} if is_sqlite else {}
pool_class = NullPool if is_sqlite else None

# Create core Async database engines
engine = create_async_engine(
    DATABASE_URL,
    connect_args=connect_args,
    poolclass=pool_class,
    echo=False
)

# Async session maker builder
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def init_db() -> None:
    """Initialize base tables for local SQLite operations"""
    from ..models.database import Base
    if is_sqlite:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injector helper to retrieve database sessions"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
