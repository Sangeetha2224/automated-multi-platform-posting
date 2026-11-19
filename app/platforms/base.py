
from abc import ABC, abstractmethod


class BasePlatform(ABC):

    @abstractmethod
    async def post(self, message: str) -> dict:
        """
        Publish a message to a platform.
        Each platform must implement this method.
        """
        pass
