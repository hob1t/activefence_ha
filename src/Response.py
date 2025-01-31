from dataclasses import dataclass


@dataclass
class Response:
    allowed: bool
    """
    Indicates allow to pass request or not
    """
    limit: int
    """
    Allowed maximum requests per window
    """
    remaining: int
    """
    How many requests are remaining
    """
    reset: float
    """
    Unix timestamp, like date +%s
    """
