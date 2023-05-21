from contextlib import asynccontextmanager, AbstractAsyncContextManager
from typing import Callable
import asyncio

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session, async_sessionmaker,\
    AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Database:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.engine = create_async_engine(self.db_url, echo=True)
        self.session_factory = async_scoped_session(
            async_sessionmaker(
                autoflush=False,
                bind=self.engine,
                class_=AsyncSession
            ),
            asyncio.current_task
        )

    async def drop_models(self):
        engine = create_async_engine(self.db_url, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    async def init_models(self):
        engine = create_async_engine(self.db_url, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
