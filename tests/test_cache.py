from src.cache import ResponseCache


def test_cache_set_and_get():
    cache = ResponseCache()

    cache.set("test", "result")

    assert cache.get("test") == "result"


def test_cache_contains():
    cache = ResponseCache()

    assert not cache.contains("test")

    cache.set("test", "result")

    assert cache.contains("test")


def test_cache_clear():
    cache = ResponseCache()

    cache.set("test", "result")
    cache.clear()

    assert not cache.contains("test")
    assert cache.get("test") is None
