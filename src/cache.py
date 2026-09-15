from typing import Any


class ResponseCache:
    def __init__(self):
        self._cache: dict[str, Any] = {}

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def contains(self, key: str) -> bool:
        return key in self._cache

    def clear(self) -> None:
        self._cache.clear()
