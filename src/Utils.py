import time
from redis import Redis
from src.Typing import UnitT


def ms_to_s(value: int) -> float:
    return value / 1_000


def now_ms() -> int:
    return int(time.time() * 1_000)


def to_ms(value: int, unit: UnitT) -> int:
    if unit == "ms":
        return value
    elif unit == "s":
        return value * 1_000
    elif unit == "m":
        return value * 60 * 1_000
    elif unit == "h":
        return value * 60 * 60 * 1_000
    elif unit == "d":
        return value * 24 * 60 * 60 * 1_000
    else:
        raise ValueError("Unsupported unit")


def now_s() -> float:
    return time.time()


def clear_ns(redis: Redis):
    redis.flushall()


def check_key_and_renew(redis_client: Redis, key: str, window: int):
    if redis_client.exists(repr(key)) == 0:
        redis_client.delete(key)
        redis_client.set(repr(key), str(window))
        redis_client.expire(repr(key), window, 'XX')
        print(f"key is renewed")
