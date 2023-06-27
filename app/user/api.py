from datetime import timedelta

from flask import Blueprint
from flask.typing import ResponseReturnValue
from sqlalchemy import or_

from app.core.auth import User, current_user, login_required
from app.core.exception import Created, ParameterException, Success, Updated
from app.core.schema import validate
from app.user.model import CodeRedis, clear_mobile_cache, clear_name_cache
from app.util.const import CodeCate
from app.util.util import generate_digit_code
from sms.tasks import send_sms

from .schema import CodeSchema, ForgetSchema, NameSchema, RegisterSchema, ResetSchema

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/code")
@validate
def get_code(query: CodeSchema) -> ResponseReturnValue:
    """获取验证码."""
    code = generate_digit_code()
    ttl = timedelta(minutes=60)
    # redis 存储验证码
    CodeRedis(query.mobile, query.cate).set(code, ttl)
    # sms 发送验证码
    send_sms.delay(query.mobile, code, int(ttl.total_seconds()))
    return Success(message="验证码发送成功")


@bp.get("/name")
@validate
def get_name(query: NameSchema) -> ResponseReturnValue:
    """获取昵称是否存在."""
    return {"is_valid": True}


@bp.post("/register")
@validate
def register(body: RegisterSchema) -> ResponseReturnValue:
    """注册."""
    code = CodeRedis(body.mobile, CodeCate.REGISTER).get()
    if body.code != code:
        raise ParameterException(message="验证码不正确 请重试")

    user = User.get_by_attr(or_(User.username == body.username, User.mobile == body.mobile), User.is_deleted == 0)
    if user:
        raise ParameterException(message="用户名或手机号已存在, 请更换")
    user = User(username=body.username, mobile=body.mobile)
    user.set_password(body.password)
    user.save()
    # 清楚手机缓存和用户名缓存
    clear_mobile_cache(body.mobile)
    clear_name_cache(body.username)
    return Created(message="注册成功")


# login 在 app/core/auth/auth.py 中实现


@bp.post("/forget")
@validate
def forget(body: ForgetSchema) -> ResponseReturnValue:
    """忘记密码."""
    code = CodeRedis(body.mobile, CodeCate.FORGET).get()
    if body.code != code:
        raise ParameterException(message="验证码不正确 请重试")

    user = User.get_by_attr(User.mobile == body.mobile, User.is_deleted == 0)
    if not user:
        raise ParameterException(message="手机号未注册")
    user.set_password(body.password)
    user.save()

    return Updated(message="修改成功")


@bp.post("/reset")
@login_required
@validate
def reset(body: ResetSchema) -> ResponseReturnValue:
    """修改密码."""
    user = current_user.get()
    if user is None:
        raise ParameterException(message="用户不存在")
    if not user.check_password(body.old_password):
        raise ParameterException(message="旧密码错误")
    user.set_password(body.password)
    user.save()

    return Updated(message="修改成功")


@bp.get("/<int:user_id>/info")
def info(user_id: int) -> ResponseReturnValue:
    """获取用户信息."""
    user = User.get_by_attr(User.id == user_id, User.is_deleted == 0)
    if user is None:
        raise ParameterException(message="用户不存在")
    return user.to_dict(exclude_field={"password", "is_deleted", "status"})
