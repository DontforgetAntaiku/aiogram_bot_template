from tortoise import Tortoise, run_async

from app.config import Config
from app.services.classes import SingletonFactory

config = Config()

user, password, host, port, dbname = (
    config.database.USER,
    config.database.PASSWORD,
    config.database.HOST,
    config.database.PORT,
    config.database.NAME,
)


TORTOISE_ORM = {
    "connections": {"default": f"postgres://{user}:{password}@{host}:{port}/{dbname}"},
    "apps": {
        "models": {
            "models": ["app.database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "_create_db": True,
}

class DB(SingletonFactory):
    def init(self):
        run_async(self.init_db())

    async def init_db(self):
        await Tortoise.init(
            config=TORTOISE_ORM
        )
        await Tortoise.generate_schemas()

    async def close_db(self):
        await Tortoise.close_connections()



__all__ = ['TORTOISE_ORM', 'DB']