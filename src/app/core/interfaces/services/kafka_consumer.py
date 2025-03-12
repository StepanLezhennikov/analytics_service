from abc import ABC, abstractmethod


class ConsumerServiceInterface(ABC):
    @abstractmethod
    async def consume(self):
        pass
