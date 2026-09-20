import asyncio
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config.settings import settings

_client: Optional[AsyncIOMotorClient] = None
_client_loop: Optional[asyncio.AbstractEventLoop] = None


def get_client() -> AsyncIOMotorClient:
    global _client, _client_loop
    try:
        current_loop = asyncio.get_running_loop()
    except RuntimeError:
        current_loop = None

    if _client is None or (_client_loop is not None and current_loop is not None and _client_loop != current_loop):
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
        _client_loop = current_loop

    return _client


class DatabaseProxy:
    """
    Transparent proxy to ensure Motor collections always execute on the active event loop,
    preventing 'Event loop is closed' errors during multi-test pytest-asyncio runs.
    """
    def __getattr__(self, name: str):
        return getattr(get_client().ai_interview_system, name)

    def __getitem__(self, name: str):
        return get_client().ai_interview_system[name]


db = DatabaseProxy()
client = db