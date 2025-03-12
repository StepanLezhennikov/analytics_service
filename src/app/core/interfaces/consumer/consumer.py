from abc import ABC, abstractmethod


class ConsumerInterface(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def __aiter__(self):
        pass

    @abstractmethod
    async def __anext__(self):
        pass
