import inspect
from typing import Any, Awaitable, Callable

from aiohttp import web


def inject(handler: Callable[..., Awaitable[Any]]):
    sig = inspect.signature(handler)

    async def wrapper(request: web.Request, *args, **kwargs) -> Any:
        # Extract dependencies based on parameter names
        dependencies = {
            param: request[param] for param in sig.parameters if param in request
        }
        # Call the original handler with dependencies
        return await handler(request, *args, **dependencies)

    return wrapper


@web.middleware
class InjectMiddleware:
    def __init__(self, **kwargs) -> None:
        self.dependencies = kwargs

    async def __call__(
        self,
        request: web.Request,
        handler: Callable[[web.Request], Awaitable[web.Response]],
    ) -> web.Response:
        # Inject all dependencies into the request
        for key, value in self.dependencies.items():
            request[key] = value
        # Call the next handler
        response = await handler(request)
        return response
