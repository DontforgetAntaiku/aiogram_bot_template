from aiohttp import web
from tgbot.db.database import DB


@web.middleware
class WebDbMiddleware:
    def __init__(self, db: DB):
        self.db = db

    async def __call__(self, request: web.Request, handler):
        async with self.db.get_session() as session:
            request["db_session"] = session  # Inject db session into request
            response = await handler(request)
            return response
