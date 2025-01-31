import time
import redis
from src.TokenBucket import TokenBucket
from src.RateLimiter import RateLimiter
from src.Utils import clear_ns

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def test_token_buket_strategy() -> None:
    clear_ns(redis_client)
    key = f"token_buket:{time.time()}"
    token_buket = TokenBucket(key, 5, 150)
    rate_limiter = RateLimiter(token_buket)

    for i in range(50):
        response = rate_limiter.rate_limit()
        print(f"\ntoken buket algo: {response}")
        assert response
        time.sleep(30)
