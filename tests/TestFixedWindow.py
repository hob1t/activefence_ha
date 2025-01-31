import time
import uuid
import redis
from src.FixedWindow import FixedWindow
from src.RateLimiter import RateLimiter
from src.Utils import clear_ns

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def test_fixed_window_strategy() -> None:
    clear_ns(redis_client)
    key = f"@oleg_af/ratelimit:{random_id()}"
    fixed_window = FixedWindow(key, 5, 150)
    rate_limiter = RateLimiter(fixed_window)

    for i in range(50):
        response = rate_limiter.rate_limit()
        print(f"\nfixed window algo: {response}")
        assert response
        time.sleep(30)


def random_id() -> str:
    return str(uuid.uuid4())
