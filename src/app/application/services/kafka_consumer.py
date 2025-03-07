import logging

from aiokafka import AIOKafkaConsumer

from app.config import config
from app.presentation.interfaces.services.kafka_consumer import (
    KafkaConsumerServiceInterface,
)

logger = logging.getLogger("main")

logger.setLevel(logging.INFO)


class KafkaConsumerService(KafkaConsumerServiceInterface):

    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            "create_task",
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            group_id="analytics",
        )

    async def start_consuming(self):
        await self.consumer.start()

    async def consume(self):
        if self.consumer:
            async for message in self.consumer:
                logger.info(f"Received message: {message.value}")

    async def stop_consuming(self):
        if self.consumer:
            await self.consumer.stop()
