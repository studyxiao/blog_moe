import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel, validator

from app.core.exception import ParameterException
from app.util.const import CodeCate

from .model import CodeRedis, mobile_existed, name_existed

# 手机号:11位大陆手机号,包括虚拟运营商
mobile_pattern = r"^(13[0-9]|14[014-9]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[^4])\d{8}$"
# 用户昵称:4-12位,只能是字母汉字和数字,且不能以数字开头
username_pattern = r"^[a-zA-z\u4e00-\u9fa5][0-9a-zA-z\u4e00-\u9fa5]{3,11}"
# 密码: 6-20位,包含大小写字母、数字和特殊符号
password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@!,\.*?&%])[a-zA-Z0-9@!,\.*?&%]{6,20}$"  # noqa: S105
# 电子邮箱
email_pattern = r"^\W+([-+.]\W+)*@\W+([-.]\W+)*.\W+([-.]\W+)*$"


def _check_mobile_re(val: str) -> None:
    if not re.match(mobile_pattern, val):
        raise ParameterException(message="手机号格式不正确")


class CodeSchema(BaseModel):
    """手机获取验证码."""

    cate: CodeCate
    mobile: str

    @validator("mobile")
    def check_mobile(cls, val: str, values: dict[str, Any], **kwargs: Any) -> str:
        """验证手机号格式以及是否注册."""
        _check_mobile_re(val)
        if values.get("cate") is None:
            raise ValueError("请填写验证码类型")
        if values["cate"] == CodeCate.REGISTER:
            if mobile_existed(val):
                raise ValueError("手机已注册")
        else:
            if not mobile_existed(val):
                raise ValueError("手机未注册")
        code_redis = CodeRedis(val, values["cate"])
        if code_redis.get() is not None:
            # 已经发送过验证码
            raise ValueError("请稍后获取验证码")
        return val


class NameSchema(BaseModel):
    username: str

    @validator("username")
    def check_name(cls, val: str) -> str:
        if not re.match(username_pattern, val):
            raise ValueError("只能是字母汉字和数字,且不能以数字开头的4-12字符之间")
        if name_existed(val):
            raise ValueError("昵称已存在")
        return val


class ValidName(BaseModel):
    is_valid: bool = True


class RegisterSchema(BaseModel):
    mobile: str
    password: str
    password2: str
    code: str
    username: str

    @validator("mobile")
    def check_mobile(cls, val: str) -> str:
        _check_mobile_re(val)
        # 是否已注册
        if mobile_existed(val):
            raise ValueError("手机号已存在")
        return val

    @validator("password")
    def check_password(cls, val: str) -> str:
        if not re.match(password_pattern, val):
            raise ValueError("密码格式不正确")
        return val

    @validator("password2")
    def check_password2(cls, val: str, values: dict[str, Any]) -> str:
        if "password" in values and val != values["password"]:
            raise ValueError("两次密码不一致")
        return val

    @validator("code")
    def check_code(cls, val: str, values: dict[str, Any]) -> str:
        if len(val) != 6 or (not val.isdigit()):
            raise ValueError("验证码不正确")
        if "mobile" in values and val != CodeRedis(values["mobile"], CodeCate.REGISTER).get():
            raise ValueError("验证码错误")
        return val

    @validator("username")
    def check_name(cls, val: str) -> str:
        if not re.match(username_pattern, val):
            raise ValueError("只能是字母汉字和数字,且不能以数字开头的4-12字符之间")
        if name_existed(val):
            raise ValueError("昵称已存在")
        return val


class Forget(BaseModel):
    mobile: str
    password: str
    password2: str
    code: str

    @validator("mobile")
    def check_mobile(cls, val: str) -> str:
        _check_mobile_re(val)
        # 是否已注册
        if not mobile_existed(val):
            raise ValueError("手机号不存在")
        return val

    @validator("password")
    def check_password(cls, val: str) -> str:
        if not re.match(password_pattern, val):
            raise ValueError("密码格式不正确")
        return val

    @validator("password2")
    def check_password2(cls, val: str, values: dict[str, Any]) -> str:
        if "password" in values and val != values["password"]:
            raise ValueError("两次密码不一致")
        return val

    @validator("code")
    def check_code(cls, v: str, values: dict[str, Any]) -> str:
        if len(v) != 6 or (not v.isdigit()):
            raise ValueError("验证码不正确")
        if "mobile" in values and v != CodeRedis(values["mobile"], CodeCate.FORGET).get():
            raise ValueError("验证码错误")
        return v


class LoginByMobile(BaseModel):
    mobile: str
    cate: int
    certificate: str

    @validator("mobile")
    def check_mobile(cls, val: str) -> str:
        _check_mobile_re(val)
        return val


class Reset(BaseModel):
    old_password: str
    password: str
    password2: str

    @validator("old_password")
    def check_old_password(cls, val: str) -> str:
        if not re.match(password_pattern, val):
            raise ValueError("密码格式不正确")
        return val

    @validator("password")
    def check_password(cls, val: str) -> str:
        if not re.match(password_pattern, val):
            raise ValueError("密码格式不正确")
        return val

    @validator("password2")
    def check_password2(cls, val: str, values: dict[str, Any]) -> str:
        if "password" in values and val != values["password"]:
            raise ValueError("两次密码不一致")
        return val


class ChangeUser(BaseModel):
    username: str
    gender: int | None
    birthday: datetime | None
    email: str | None
    address: str | None
    signature: str | None

    @validator("username")
    def check_name(cls, val: str) -> str:
        if not re.match(username_pattern, val):
            raise ValueError("只能是字母汉字和数字,且不能以数字开头的4-12字符之间")
        if name_existed(val):
            raise ValueError("昵称已存在")
        return val

    @validator("gender")
    def check_gender(cls, val: int) -> int:
        if val and (val < 0 or val > 3):
            raise ParameterException(message="性别设置错误")
        return val

    @validator("email")
    def check_email(cls, val: str) -> str:
        if val and not re.match(email_pattern, val):
            raise ParameterException(message="电子邮箱格式错误")
        return val
