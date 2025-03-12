import json
import logging

from fastapi import Depends
from aiokafka import AIOKafkaConsumer
from dependency_injector.wiring import Provide, inject

from app.config import TOPICS, config
from app.core.interfaces.repositories.message import MessageRepositoryInterface
from app.core.interfaces.services.kafka_consumer import KafkaConsumerServiceInterface

logger = logging.getLogger("kafka_consumer")

logger.setLevel(logging.DEBUG)


class KafkaConsumerService(KafkaConsumerServiceInterface):

    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            TOPICS.TASK_CREATED.value,
            TOPICS.TASK_UPDATED.value,
            TOPICS.TASK_DELETED.value,
            TOPICS.PROJECT_CREATED.value,
            TOPICS.PROJECT_DELETED.value,
            TOPICS.PROJECT_UPDATED.value,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            group_id="analytics",
        )

    async def start_consuming(self):
        await self.consumer.start()

    @inject
    async def consume(
        self,
        message_repository: MessageRepositoryInterface = Depends(
            Provide["message_repository"]
        ),
    ):
        if self.consumer:
            async for message in self.consumer:
                message_str = message.value.decode("utf-8")

                try:
                    message_data = json.loads(message_str)
                    logger.info(f"Topic: {message.topic}")
                    logger.info(f"Parsed message data: {message_data}")

                    await message_repository.create(TOPICS(message.topic), message_data)

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

    async def stop_consuming(self):
        if self.consumer:
            await self.consumer.stop()
