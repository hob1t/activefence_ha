from src.Strategy import Strategy, redis_client
from src.Response import Response
from src.Typing import UnitT
from src.Utils import now_s, check_key_and_renew
from src.Config import get_pro_plan_daily_limit


class SlidingWindow(Strategy):
    """
    Combined approach of sliding logs and fixed window with lower storage
    costs than sliding logs and improved boundary behavior by calculating a
    weighted score between two windows.

    Pros:
    - Good performance allows this to scale to very high loads.
    """

    def __init__(self, key: str, max_requests: int, window: int, unit: UnitT = "s") -> None:
        """
        :param key: a User_ID, used as part a key the same as Application_ID
        :param max_requests: Maximum number of requests allowed within a window
        :param window: The number of time units in a window
        :param unit: The unit of time
        """
        assert key
        assert max_requests > 0
        assert window > 0

        self._key = key
        self._max_requests = max_requests
        self._window = window
        self._reset = now_s() + window
        # saves a key/app_id
        redis_client.set(repr(self._key), str(window))
        # EXPIRE 	key-name seconds — Sets the key to expire in the given number of seconds
        redis_client.expire(repr(self._key), window, 'XX')
        redis_client.set('PRO_PLAN', get_pro_plan_daily_limit())


    def rate_limit(self) -> Response:
        current_time = now_s()
        window_start = current_time - self._window

        # counts the number of requests made within the window
        # with scores between window_start and current_time
        requests_made = redis_client.zcount(self._key, window_start, current_time)

        if requests_made < self._max_requests:
            # adds a new element to the sorted set with the current time (current_time) as the score and value
            # it indicates that a new request has been made at this timestamp
            redis_client.zadd(self._key, {current_time: current_time})
            # zremrangebyscore command to remove elements from the sorted set with scores less than or equal
            # to window_start. this ensures that only the requests within the specified window remain in the sorted set
            redis_client.zremrangebyscore(self._key, '-inf', window_start)

        print(f"requests made:{requests_made  + 1}")
        check_key_and_renew(redis_client, self._key, self._window)

        return Response(
            # if key expired we get None
            allowed=(requests_made <= self._max_requests) and (redis_client.get(repr(self._key)) is not None),
            limit=self._max_requests,
            remaining=redis_client.decrby('PRO_PLAN'),
            reset=self._reset,
        )
