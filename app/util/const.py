from enum import Enum, IntEnum


class CodeCate(Enum):
    REGISTER = "register"  # 注册时
    LOGIN = "login"  # 登录时
    FORGET = "forget"  # 忘记密码
    RESET = "reset"  # 重置密码


class Source(IntEnum):
    YUANCHUANG = 1  # 原创
    FANYI = 2  # 翻译
    ZHUANZAI = 3  # 转载
