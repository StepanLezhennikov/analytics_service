from abc import ABC, abstractmethod

from app.config import TOPICS


class MessageProcessInterface(ABC):
    @abstractmethod
    async def process_message(self, topic: TOPICS, message: str) -> None:
        pass
