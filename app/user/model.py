from datetime import datetime, timedelta

from pydantic import BaseModel

from app.core.auth.model import User
from app.core.exception import ServerError
from app.util.const import CodeCate
from service.cache import Node, cache
from service.logger import logger
from service.redis import redis


class CodeModel(BaseModel):
    """验证码模型."""

    type: str
    mobile: str
    code: str
    expire: datetime


class CodeRedis:
    """验证码 redis 操作."""

    def __init__(self, mobile: str, cate: CodeCate) -> None:
        self.name = cate.value + ":" + mobile

    def get(self) -> str | None:
        """从 redis 获得验证码,如果存在则表示已经发送."""
        return redis.get(self.name)

    def set(self, code: str, expire: timedelta = timedelta(minutes=5)) -> bool:
        """在 redis 中保存验证码,并设置过期时间(默认5分钟)."""
        res = redis.set(self.name, code, ex=expire)
        if not res:
            # TODO redis 存储失败处理
            logger.error("redis 存储失败")
            raise ServerError(message="redis 存储失败")
        return True


class NameModel(BaseModel):
    """昵称模型."""

    name: str


class NameNode(Node[NameModel]):
    """昵称缓存节点."""

    storages = [  # noqa: RUF012
        {"storage": "redis", "ttl": timedelta(days=1)},
    ]

    def __init__(self, name: str) -> None:
        self.name = name

    def key(self) -> str:
        return self.name

    def load(self) -> NameModel | None:
        user = User.get_by_attr(User.username == self.name, User.is_deleted == 0)
        if user:
            return NameModel(name=user.username)
        return None


def name_existed(name: str) -> bool:
    """查询昵称是否存在.

    会先从缓存中查询,如果缓存中不存在则从数据库中查询,并将查询结果缓存.
    """
    node = NameNode(name)
    model = cache.get(node)
    if model is None:
        return False
    return True


class MobileModel(BaseModel):
    """昵称模型."""

    mobile: str


class MobileNode(Node[MobileModel]):
    """昵称缓存节点."""

    storages = [  # noqa: RUF012
        {"storage": "redis", "ttl": timedelta(days=1)},
    ]

    def __init__(self, mobile: str) -> None:
        self.mobile = mobile

    def key(self) -> str:
        return self.mobile

    def load(self) -> MobileModel | None:
        user = User.get_by_attr(User.mobile == self.mobile, User.is_deleted == 0)
        if user:
            return MobileModel(mobile=user.mobile)
        return None


def mobile_existed(mobile: str) -> bool:
    """检查手机号是否已经注册."""
    node = MobileNode(mobile)
    model = cache.get(node)
    if model is None:
        return False
    return True


def clear_mobile_cache(mobile: str) -> None:
    """清除手机号缓存."""
    node = MobileNode(mobile)
    cache.remove(node, "redis")


def clear_name_cache(name: str) -> None:
    """清除昵称缓存."""
    node = NameNode(name)
    cache.remove(node, "redis")


def user_existed(id: int) -> bool:
    """检查用户是否存在."""
    user = User.get_by_attr(User.id == id, User.is_deleted == 0)
    if user:
        return True
    return False
