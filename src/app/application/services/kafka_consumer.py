import json
import logging

from aiokafka import AIOKafkaConsumer

from app.config import config
from app.presentation.interfaces.services.kafka_consumer import ConsumerServiceInterface

logger = logging.getLogger("kafka_consumer")

logger.setLevel(logging.INFO)


class KafkaConsumerService(ConsumerServiceInterface):
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            config.KAFKA_TOPIC_CREATE_TASK,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            group_id="analytics",
        )

    async def __aenter__(self):
        logger.info("Starting Kafka Consumer with context manager...")
        await self.consumer.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        logger.info("Stopping Kafka Consumer...")
        await self.consumer.stop()

    async def consume(self):
        async for message in self.consumer:
            logger.info(f"Topic: {message.topic}")
            message_str = message.value.decode("utf-8")
            logger.info(f"Message: {message_str}")
            try:
                message_data = json.loads(message_str)
                logger.info(f"Parsed message data: {message_data}")
                # TODO: Запись в БД
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON: {e}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def stop_consuming(self):
        if self.consumer:
            await self.consumer.stop()
