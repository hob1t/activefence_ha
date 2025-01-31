import time
import uuid
import redis
from src.SlidingWindow import SlidingWindow
from src.RateLimiter import RateLimiter
from src.Utils import clear_ns

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def test_sliding_window_strategy() -> None:
    clear_ns(redis_client)
    key = f"@oleg_af/ratelimit:{random_id()}"
    sliding_window = SlidingWindow(key, 5, 150)
    rate_limiter = RateLimiter(sliding_window)

    for i in range(15):
        response = rate_limiter.rate_limit()
        print(f"\nsliding window algo: {response}")
        assert response
        time.sleep(30)


def random_id() -> str:
    return str(uuid.uuid4())
