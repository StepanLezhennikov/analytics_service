import json
import logging

from fastapi import Depends
from dependency_injector.wiring import Provide

from app.config import TOPICS
from app.core.schemas.topics import (
    TaskCreated,
    TaskDeleted,
    TaskUpdated,
    UserCreated,
    UserDeleted,
    ProjectCreated,
    ProjectDeleted,
)
from app.core.interfaces.repositories.message import MessageRepositoryInterface
from app.core.interfaces.services.message_handler import MessageHandlerInterface

logger = logging.getLogger("message_process_service")
logger.setLevel(logging.INFO)


def convert_datetime_fields(topic: TOPICS, data: dict):
    match topic:
        case TOPICS.TASK_UPDATED.value:
            data = TaskUpdated.model_validate(data)

        case TOPICS.TASK_CREATED.value:
            data = TaskCreated.model_validate(data)

        case TOPICS.TASK_DELETED.value:
            data = TaskDeleted.model_validate(data)

        case TOPICS.PROJECT_CREATED.value:
            data = ProjectCreated.model_validate(data)

        case TOPICS.PROJECT_DELETED.value:
            data = ProjectDeleted.model_validate(data)

        case TOPICS.USER_CREATED.value:
            data = UserCreated.model_validate(data)

        case TOPICS.USER_DELETED.value:
            data = UserDeleted.model_validate(data)
        case _:
            raise ValueError("Invalid topic")

    return data.model_dump()


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

            message_data = convert_datetime_fields(TOPICS(topic), message_data)

            logger.info(f"Parsed message data: {message_data}")

            await self.message_repository.create(TOPICS(topic), message_data)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
        except ValueError as e:
            logger.error(f"Error parsing message data: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
