"""Database helpers and session initialization for the app.

This module creates the async SQLAlchemy engine and a session factory used by
other parts of the application. It also exposes `init_db` which will create
SQL tables for local development convenience when Alembic migrations are not
being run.

Environment variables:
- DATABASE_URL: Async SQLAlchemy database url, e.g. postgresql+asyncpg://user:pass@host:5432/db

Important notes:
- Alembic doesn't support the asyncpg driver directly for migrations. Our alembic
  env.py strips the +asyncpg suffix when running migrations so Alembic uses the
  sync driver. When running the app, the async engine (asyncpg) is used.

"""
from typing import AsyncGenerator
import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

# Read the DATABASE_URL from environment or fall back to a sane default useful for
# local development. The URL should include the asyncpg driver when used by the
# running application.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/demo")

# Create an async engine and an async sessionmaker. We set expire_on_commit=False
# to avoid expired objects after commit in async context which simplifies tests
# and common patterns where the object is accessed after commit/refresh.
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for use in FastAPI dependencies.

    Example:
        async def route(session: AsyncSession = Depends(get_session)):
            await session.exec(select(...))
    """
    async with async_session() as session:
        yield session

async def init_db():
    """Create database tables from SQLModel metadata.

    For production the preferred workflow is to use Alembic migrations. This
    helper is convenient for local development and tests where running migrations
    may be intentionally skipped.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
