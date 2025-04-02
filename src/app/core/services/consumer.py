import logging

from fastapi import Depends
from dependency_injector.wiring import Provide, inject

from app.config import TOPICS
from app.core.interfaces.consumer.consumer import ConsumerInterface
from app.core.interfaces.services.consumer import ConsumerServiceInterface
from app.core.interfaces.repositories.message import MessageRepositoryInterface
from app.core.interfaces.services.message_handler import MessageHandlerInterface

logger = logging.getLogger("consumer")


class ConsumerService(ConsumerServiceInterface):
    def __init__(
        self,
        message_process_service: MessageHandlerInterface = Depends(
            Provide["message_process_service"]
        ),
        consumer: ConsumerInterface = Depends(Provide["consumer"]),
    ):
        self.consumer = consumer
        self.message_process_service = message_process_service

    async def __aenter__(self):
        logger.info("Starting Consumer...")
        await self.consumer.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        logger.info("Stopping Consumer...")
        await self.consumer.stop()

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
                await self.message_process_service.handle_message(
                    TOPICS(message.topic), message_str
                )
