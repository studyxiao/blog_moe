from app.core.cache import Manager, Node, RedisStorage

from .redis import redis_bytes as redis

cache = Manager()
cache.register_storage("redis", RedisStorage(redis))

__all__ = (
    "cache",
    "Node",
)
