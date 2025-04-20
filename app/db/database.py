from tortoise import Tortoise, run_async

from app.services.classes import SingletonFactory


class DB(SingletonFactory):
    def init(self, user, password, dbname, host, port):
        self.connection_string = f"postgres://{user}:{password}@{host}:{port}/{dbname}"
        run_async(self.init_db())

    async def init_db(self):
        await Tortoise.init(
            db_url=self.connection_string,
            modules={"models": ["app.db.models"]},
        )
        await Tortoise.generate_schemas()

    async def close_db(self):
        await Tortoise.close_connections()
