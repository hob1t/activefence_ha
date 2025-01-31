from abc import ABC, abstractmethod
from src.Response import Response
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def rate_limit(self) -> Response:
        pass
