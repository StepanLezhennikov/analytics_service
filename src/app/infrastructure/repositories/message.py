from app.config import TOPICS
from app.db_config import db
from app.core.services.consumer import logger
from app.core.interfaces.repositories.message import MessageRepositoryInterface


class MessageRepository(MessageRepositoryInterface):
    async def create(self, collection: TOPICS, message: dict) -> None:
        collection = getattr(db, collection.value)
        logger.info(collection.find())
        logger.info(f"Collection: {collection}")
        await collection.insert_one(message)
