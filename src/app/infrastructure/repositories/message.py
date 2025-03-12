from app.config import TOPICS
from app.db_config import db
from app.application.services.kafka_consumer import logger
from app.application.interfaces.repositories.message import MessageRepositoryInterface


class MessageRepository(MessageRepositoryInterface):
    async def create(self, collection: TOPICS, message: dict) -> None:
        collection = getattr(db, collection.value)
        logger.info(collection.find())
        logger.info(f"Collection: {collection}")
        await collection.insert_one(message)
