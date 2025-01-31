from src.Response import Response


def test_response() -> None:
    res = Response(True, 100, 99, 1737998988)
    assert res
