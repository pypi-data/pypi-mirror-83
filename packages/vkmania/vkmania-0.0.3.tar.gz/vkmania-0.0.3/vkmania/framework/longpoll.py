import typing

from abc import ABC, abstractmethod

class Longpoll(ABC):
    server: dict
    wait: int
    version: int = None

    @abstractmethod
    def get_server(self) -> dict:
        pass

    @abstractmethod
    async def run(self, longpoll_server: dict) -> None:
        pass

    @abstractmethod
    def start_longpoll(self) -> None:
        pass

    def stop(self) -> None:
        pass