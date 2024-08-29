from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tgbot.classes.singleton import Singleton
from tgbot.db.models import Base


class DB(Singleton):
    def init(self, user, password, dbname, host, port):
        self.connection_string = (
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
        )

        self.engine = create_async_engine(
            url=self.connection_string,
            # echo=True,
        )
        self.AsyncLocalSession = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )
        try:
            self.AsyncLocalSession()
        except Exception as e:
            print(e)
            exit()

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.AsyncLocalSession() as session:
            yield session
