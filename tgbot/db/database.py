import aiosqlite

from tgbot.classes.singleton import Singleton


class MyDb(Singleton):
    __dbname__ = "db.db"

    async def db_setup(self):
        async with aiosqlite.connect(self.__dbname__) as db:
            async with db.cursor() as cursor:
                await db.commit()


# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from tgbot.classes.singleton import Singleton
# from tgbot.db.models import Base
# class DB(Singleton):
#     def init(
#         self,
#     ):
#         self.connection_string = "sqlite+aiosqlite:///./db.db"

#         self.engine = create_async_engine(
#             url=self.connection_string,
#             echo=True,
#         )
#         self.AsyncLocalSession = sessionmaker(
#             autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
#         )

#     async def create_tables(self):
#         async with self.engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)

#     async def get_session(self):
#         async with self.AsyncLocalSession() as session:
#             return session
