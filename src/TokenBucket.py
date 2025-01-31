from src.Strategy import Strategy, redis_client
from src.Response import Response
from src.Typing import UnitT
from src.Utils import now_s, check_key_and_renew
import time


class TokenBucket(Strategy):
    """
    A bucket is filled with maximum number of tokens that refill at a given
    rate per interval.

    Each request tries to consume one token and if the bucket is empty,
    the request is rejected.

    Pros:
    - Bursts of requests are smoothed out so that they can be processed at
      a constant rate.
    - Allows to set a higher initial burst limit by setting maximum number
      of tokens higher than the refill rate.
    """

    #                  key, capacity, tokens_per_second
    def __init__(self, key: str, max_requests: int, window: int, unit: UnitT = "s") -> None:
        """
        :param key: a User_ID, used as part a key the same as Application_ID
        :param max_requests: Maximum number of requests allowed within a window
        :param window: timeslot window
        :param unit: The unit of time - Optional
        """
        assert key
        assert max_requests > 0
        assert window > 0

        self._key = key
        self._max_tokens = max_requests
        self._refill_rate = window
        self._reset = now_s() + window

        # EXPIRE key-name seconds — Sets the key to expire in the given number of seconds
        redis_client.set(repr(self._key), str(window))
        redis_client.expire(repr(self._key), window, 'XX')  # time.now() + window

    def rate_limit(self) -> Response:
        current_time = time.time()
        last_refill_time = redis_client.hget(self._key, 'last_refill_time') or current_time
        tokens = int(redis_client.hget(self._key, 'tokens') or self._max_tokens)
        elapsed_time = current_time - float(last_refill_time)
        new_tokens = int(elapsed_time * self._refill_rate)

        if tokens == 0:  # refill
            tokens = min(new_tokens, self._max_tokens)

        redis_client.hset(self._key, 'tokens', tokens)
        redis_client.hset(self._key, 'last_refill_time', current_time)

        if tokens > 0:  # consumes a token
            redis_client.hincrby(self._key, 'tokens', -1)

        print(f"{redis_client.exists(repr(self._key))} {time.ctime()}")
        # updates reset if needed
        self.check_and_fix_reset()
        # updates to the new window
        check_key_and_renew(redis_client, self._key, self._refill_rate)


        return Response(
            # if tokens > 0 True
            allowed=(tokens > 0) and (redis_client.get(repr(self._key)) is not None),
            limit=self._max_tokens,
            remaining=(0 if tokens < 0 else tokens),
            reset=self._reset,
        )

    def check_and_fix_reset(self) -> float:
        if redis_client.exists(repr(self._key)) == 0:
            self._reset = now_s() + self._refill_rate
        return self._reset