from abc import ABC, abstractmethod


class ConsumerServiceInterface(ABC):

    # @abstractmethod
    # async def start_consuming(self):
    #     pass

    @abstractmethod
    async def consume(self):
        pass

    # @abstractmethod
    # async def stop_consuming(self):
    #     pass
