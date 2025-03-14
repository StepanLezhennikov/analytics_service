from aiokafka import AIOKafkaConsumer
from dependency_injector import providers, containers

from app.config import TOPICS, config
from app.infrastructure.repositories.message import MessageRepository
from app.infrastructure.services.message_handler import MessageHandler

topics = [
    TOPICS.TASK_CREATED.value,
    TOPICS.TASK_UPDATED.value,
    TOPICS.TASK_DELETED.value,
    TOPICS.PROJECT_CREATED.value,
    TOPICS.PROJECT_DELETED.value,
    TOPICS.USER_ADDED.value,
    TOPICS.USER_DELETED.value,
]


class Container(containers.DeclarativeContainer):
    message_repository = providers.Singleton(MessageRepository)
    message_process_service = providers.Factory(
        MessageHandler, message_repository=message_repository
    )
    consumer = providers.Factory(
        AIOKafkaConsumer,
        *topics,
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        group_id="analytics"
    )
