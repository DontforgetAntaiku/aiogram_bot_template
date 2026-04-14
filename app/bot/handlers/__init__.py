from .user import router as user_router

BOT_ROUTERS_LIST = (user_router,)


__all__ = ("BOT_ROUTERS_LIST",)
