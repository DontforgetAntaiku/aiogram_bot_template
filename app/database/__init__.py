from app.core import CONFIG

user, password, host, port, dbname = (
    CONFIG.database.USER,
    CONFIG.database.PASSWORD,
    CONFIG.database.HOST,
    CONFIG.database.PORT,
    CONFIG.database.NAME,
)


TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{user}:{password}@{host}:{port}/{dbname}",
        # "mysql": f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_dbname}",
    },
    "apps": {
        "models": {
            "models": [
                "app.database.models",
            ],
            "migrations": "app.database.migrations",
            "default_connection": "default",
        },
        # "external": {
        #     "models": [
        #         "app.database.mysql_models",
        #     ],
        #     "default_connection": "mysql",
        # },
    },
    "use_tz": True,
    "_create_db": True,
}


__all__ = ("TORTOISE_ORM",)
