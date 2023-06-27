from datetime import timedelta

from flask import Blueprint
from flask.typing import ResponseReturnValue
from sqlalchemy import or_

from app.core.auth.model import User
from app.core.exception import Created, ParameterException, Success
from app.core.schema import validate
from app.user.model import CodeRedis
from app.util.const import CodeCate
from app.util.util import generate_digit_code
from sms.tasks import send_sms

from .schema import CodeSchema, NameSchema, RegisterSchema

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/code")
@validate
def get_code(query: CodeSchema) -> ResponseReturnValue:
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
    return {"is_valid": True}


@bp.post("/register")
@validate
def register(body: RegisterSchema) -> ResponseReturnValue:
    code = CodeRedis(body.mobile, CodeCate.REGISTER).get()
    if body.code != code:
        raise ParameterException(message="验证码不正确 请重试")

    user = User.get_by_attr(or_(User.username == body.username, User.mobile == body.mobile), User.is_deleted == 0)
    if user:
        raise ParameterException(message="用户名或手机号已存在, 请更换")
    user = User(username=body.username, mobile=body.mobile)
    user.set_password(body.password)
    user.save()

    return Created(message="注册成功")
