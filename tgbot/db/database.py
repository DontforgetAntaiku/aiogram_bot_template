
import aiosqlite

from tgbot.classes.singleton import Singleton


class MyDb(Singleton):
    __dbname__ = "db.db"

    async def db_setup(self):
        async with aiosqlite.connect(self.__dbname__) as db:
            async with db.cursor() as cursor:
                await db.commit()
