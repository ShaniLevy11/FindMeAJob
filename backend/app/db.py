from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.config import settings

client: AsyncMongoClient | None = None


def connect() -> None:
    global client
    client = AsyncMongoClient(settings.mongo_uri)


async def disconnect() -> None:
    if client is not None:
        await client.close()


def get_db() -> AsyncDatabase:
    assert client is not None, "Mongo client not initialised"
    return client[settings.mongo_db]
