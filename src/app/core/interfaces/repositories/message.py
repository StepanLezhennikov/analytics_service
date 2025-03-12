from abc import ABC, abstractmethod

from app.config import TOPICS


class MessageRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, collection: TOPICS, message: dict) -> None:
        pass
