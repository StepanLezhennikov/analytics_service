from dependency_injector import providers, containers

from app.infrastructure.repositories.message import MessageRepository


class Container(containers.DeclarativeContainer):
    message_repository = providers.Singleton(MessageRepository)
