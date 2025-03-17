import json
import logging
from datetime import datetime

from fastapi import Depends
from dependency_injector.wiring import Provide

from app.config import TOPICS
from app.core.interfaces.repositories.message import MessageRepositoryInterface
from app.core.interfaces.services.message_handler import MessageHandlerInterface

logger = logging.getLogger("message_process_service")
logger.setLevel(logging.INFO)


def convert_datetime_fields(data: dict):
    for key, value in data.items():
        if isinstance(value, str):
            try:
                data[key] = datetime.fromisoformat(value)
            except ValueError:
                pass
    return data


class MessageHandler(MessageHandlerInterface):
    def __init__(
        self,
        message_repository: MessageRepositoryInterface = Depends(
            Provide["message_repository"]
        ),
    ):
        self.message_repository = message_repository

    async def handle_message(self, topic: TOPICS, message: str) -> None:
        try:
            message_data = json.loads(message)
            logger.info(f"Topic: {topic}")

            message_data = convert_datetime_fields(message_data)

            logger.info(f"Parsed message data: {message_data}")

            await self.message_repository.create(TOPICS(topic), message_data)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
