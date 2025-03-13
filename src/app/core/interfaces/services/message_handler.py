from abc import ABC, abstractmethod

from app.config import TOPICS


class MessageHandlerInterface(ABC):
    @abstractmethod
    async def handle_message(self, topic: TOPICS, message: str) -> None:
        pass
