from src.settings import CACHE_TTL


class Cache(object):
    value: str
    ttl: int

    def __init__(self, value: str):
        self.value = value
        self.ttl = CACHE_TTL
