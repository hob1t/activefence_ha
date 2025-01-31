from src.Config import get_free_plan_window, get_enterprise_plan_requests, get_enterprise_plan_daily_limit
from src.Config import get_free_plan_requests
from src.Config import get_free_plan_daily_limit
from src.Config import get_pro_plan_window
from src.Config import get_pro_plan_requests
from src.Config import get_pro_plan_daily_limit
from src.Config import get_enterprise_plan_window


def test_get_free_plan_window() -> None:
    result = get_free_plan_window()
    print(f"free plan window: {result}")
    assert result == 5


def test_get_free_plan_requests() -> None:
    result = get_free_plan_requests()
    print(f"free plan allowed amount of requests per window: {result}")
    assert result == 1


def test_get_free_daily_limit() -> None:
    result = get_free_plan_daily_limit()
    print(f"free plan daily limit: {result}")
    assert result == 50


#### Pro section
def test_get_pro_plan_window() -> None:
    result = get_pro_plan_window()
    print(f"pro plan window: {result}")
    assert result == 5


def test_get_pro_plan_requests() -> None:
    result = get_pro_plan_requests()
    print(f"pro plan allowed amount of requests per window: {result}")
    assert result == 10


def test_get_pro_daily_limit() -> None:
    result = get_pro_plan_daily_limit()
    print(f"pro plan daily limit: {result}")
    assert result == 12000


def test_get_enterprise_plan_window() -> None:
    result = get_enterprise_plan_window()
    print(f"enterprise plan window: {result}")
    assert result == 5


def test_get_enterprise_plan_requests() -> None:
    result = get_enterprise_plan_requests()
    print(f"enterprise plan allowed amount of requests per window: {result}")
    assert result == 100


def test_get_enterprise_daily_limit() -> None:
    result = get_enterprise_plan_daily_limit()
    print(f"enterprise plan daily limit: {result}")
    assert result is not None
