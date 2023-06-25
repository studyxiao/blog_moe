from enum import Enum


class CodeCate(Enum):
    REGISTER = "register"  # 注册时
    LOGIN = "login"  # 登录时
    FORGET = "forget"  # 忘记密码
    RESET = "reset"  # 重置密码
