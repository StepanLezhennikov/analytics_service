from aiokafka import AIOKafkaConsumer
from dependency_injector import providers, containers

from app.config import TOPICS, Config
from app.infrastructure.services.task import TaskService
from app.infrastructure.services.user import UserService
from app.infrastructure.services.project import ProjectService
from app.infrastructure.repositories.message import MessageRepository
from app.infrastructure.services.message_handler import MessageHandler
from app.infrastructure.repositories.analytics_repo import MongoRepository

topics = [
    TOPICS.TASK_CREATED.value,
    TOPICS.TASK_UPDATED.value,
    TOPICS.TASK_DELETED.value,
    TOPICS.PROJECT_CREATED.value,
    TOPICS.PROJECT_DELETED.value,
    TOPICS.USER_CREATED.value,
    TOPICS.USER_DELETED.value,
]


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Config)

    message_repository = providers.Factory(MessageRepository, config=config)
    mongo_repository = providers.Factory(MongoRepository, config=config)

    message_process_service = providers.Factory(
        MessageHandler, analytics_repository=message_repository
    )
    project_service = providers.Factory(
        ProjectService, analytics_repository=mongo_repository
    )
    task_service = providers.Factory(TaskService, analytics_repository=mongo_repository)
    user_service = providers.Factory(UserService, analytics_repository=mongo_repository)

    consumer = providers.Factory(
        AIOKafkaConsumer,
        *topics,
        bootstrap_servers=config.provided.KAFKA_BOOTSTRAP_SERVERS,
        group_id="analytics"
    )
