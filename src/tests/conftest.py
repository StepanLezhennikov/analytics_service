import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.main import app
from app.config import Config


@pytest.fixture(scope="session", autouse=True)
def settings() -> Config:
    config = Config()
    config.MONGO_URI += "test?authSource=admin"
    config.MONGO_DATABASE = "test"
    app.container.config.override(config)
    return config


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def db(settings: Config) -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_database(settings.MONGO_DATABASE)
    return db


@pytest.fixture(scope="function", autouse=True)
async def clean_db(db: AsyncIOMotorDatabase):
    collections = await db.list_collection_names()
    for collection in collections:
        await db[collection].drop()
