from src.Strategy import Strategy, redis_client
from src.Response import Response
from src.Typing import UnitT
from src.Utils import now_s, check_key_and_renew
from src.Config import get_free_plan_daily_limit


class FixedWindow(Strategy):
    """
    The time is divided into windows of fixed length, and each request inside
    a window increases a counter.

    Once the counter reaches the maximum allowed number, all further requests
    are rejected.

    Pros:
    - old ones do not starve Newer requests.
    - Low storage cost.

    Cons:
    - A burst of requests near the boundary of a window can result in twice the
      rate of requests being processed because two windows will be filled with
      requests quickly.
    """

    def __init__(self, key: str, max_requests: int, window: int, unit: UnitT = "s") -> None:
        """
        :param key: a User_ID, used as part a key the same as Application_ID
        :param max_requests: Maximum number of requests allowed within a window
        :param window: The number of time units in a window
        :param unit: The unit of time
        :param quota_by_24h: a maximum number of requests to be made by 24h
        """
        assert key
        assert max_requests > 0
        assert window > 0

        self._key = key
        self._max_requests = max_requests
        self._window = window
        self._reset = now_s() + window

        # We have to kinds of expires:
        # 1. window is expired & ! 24h, -> update key
        # 2. window is expired & 24h expired -> update key, update mx_number_of_request & key 24 hours

        # EXPIRE 	EXPIRE key-name seconds — Sets the key to expire in the given number of seconds
        redis_client.set(repr(self._key), str(window))
        # Set a timeout on key. After the timeout has expired, the key will automatically be deleted.
        redis_client.expire(repr(self._key), window, 'XX')  # time.now() + window
        redis_client.set('FREE_PLAN', get_free_plan_daily_limit())

    def rate_limit(self) -> Response:
        current_time = now_s()
        window_start = current_time - self._window

        # counts the number of requests made within the window
        requests_made = redis_client.zcount(self._key, window_start, current_time)

        if requests_made < self._max_requests:
            # this indicates that a new request has been made at this timestamp
            # adds a new element to the sorted set with the current time as the score and value
            redis_client.zadd(self._key, {current_time: current_time})

        # renew key.
        # when a window is expired, we have to renew
        # case when window is expired
        # renew after 24h
        # we need to renew max_number_of_requests
        check_key_and_renew(redis_client, self._key, self._window)

        return Response(
            # if key expired we get None
            allowed=((requests_made <= self._max_requests) and (redis_client.get(repr(self._key)) is not None)) and (int(redis_client.get('FREE_PLAN')) > 0) ,
            limit=self._max_requests,
            remaining=redis_client.decrby('FREE_PLAN'),
            reset=self._reset,
        )
