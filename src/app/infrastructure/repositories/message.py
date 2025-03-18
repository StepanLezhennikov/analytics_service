from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import TOPICS, Config
from app.core.services.consumer import logger
from app.core.interfaces.repositories.message import MessageRepositoryInterface


class MessageRepository(MessageRepositoryInterface):
    def __init__(self, config: Config):
        self.config = config
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(config.MONGO_URI)
        self.db: AsyncIOMotorDatabase = self.client.get_database(config.MONGO_DATABASE)

    async def create(self, collection: TOPICS, message: dict) -> None:
        collection = getattr(self.db, collection.value)
        logger.info(collection.find())
        logger.info(f"Collection: {collection}")
        await collection.insert_one(message)
