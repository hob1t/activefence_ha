import abc

from redis import Redis

from src import Response


class Limiter(abc.ABC):
    @abc.abstractmethod
    def limit(self, redis: Redis, identifier: str, rate: int = 1) -> Response:
        pass

    @abc.abstractmethod
    def get_remaining(self, redis: Redis, identifier: str) -> int:
        pass

    @abc.abstractmethod
    def get_reset(self, redis: Redis, identifier: str) -> float:
        pass
