import asyncio
import json
from datetime import datetime

from tortoise import Tortoise, fields

from app.services.classes import SingletonFactory


class DB(SingletonFactory):
    def init(self, user, password, dbname, host, port):
        self.connection_string = f"postgres://{user}:{password}@{host}:{port}/{dbname}"
        asyncio.run(self.init_db())

    async def init_db(self):
        await Tortoise.init(
            db_url=self.connection_string,
            modules={"models": ["tgbot.db.models"]},
        )
        await self.handle_migrations()

    async def handle_migrations(self):
        for model in Tortoise.apps["models"].values():
            for field_name, field in model._meta.fields_map.items():
                if not field.null:
                    default_value = None
                    if isinstance(field, fields.CharField):
                        default_value = input(
                            f"Enter value for new NOT NULL field '{field_name}' (string) in {model.__name__}: "
                        )
                    elif isinstance(field, fields.IntField):
                        default_value = int(
                            input(
                                f"Enter value for new NOT NULL field '{field_name}' (int) in {model.__name__}: "
                            )
                        )
                    elif isinstance(field, fields.BigIntField):
                        default_value = int(
                            input(
                                f"Enter value for new NOT NULL field '{field_name}' (bigint) in {model.__name__}: "
                            )
                        )
                    elif isinstance(field, fields.FloatField):
                        default_value = float(
                            input(
                                f"Enter value for new NOT NULL field '{field_name}' (float) in {model.__name__}: "
                            )
                        )
                    elif isinstance(field, fields.BooleanField):
                        default_value = (
                            input(
                                f"Enter value for new NOT NULL field '{field_name}' (bool, true/false) in {model.__name__}: "
                            ).lower()
                            == "true"
                        )
                    elif isinstance(field, fields.DatetimeField):
                        default_value = datetime.utcnow()
                    elif isinstance(field, fields.JSONField):
                        default_value = json.loads(
                            input(
                                f"Enter value for new NOT NULL field '{field_name}' (JSON) in {model.__name__}: "
                            )
                        )
                    elif isinstance(field, fields.TextField):
                        default_value = input(
                            f"Enter value for new NOT NULL field '{field_name}' (text) in {model.__name__}: "
                        )
                    elif isinstance(field, fields.ListField):
                        default_value = json.loads(
                            input(
                                f"Enter value for new NOT NULL field '{field_name}' (list, format: [val1, val2, ...]) in {model.__name__}: "
                            )
                        )

                    if default_value is not None:
                        await model.all().update(**{field_name: default_value})
        await Tortoise.generate_schemas()

    async def close_db(self):
        await Tortoise.close_connections()
