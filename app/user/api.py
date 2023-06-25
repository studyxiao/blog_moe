from datetime import timedelta

from flask import Blueprint
from flask.typing import ResponseReturnValue

from app.core.schema import validate
from app.user.model import CodeRedis
from app.util.util import generate_digit_code
from sms.tasks import send_sms

from .schema import CodeSchema

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/code")
@validate
def get_code(query: CodeSchema) -> ResponseReturnValue:
    code = generate_digit_code()
    ttl = timedelta(minutes=5)
    # redis 存储验证码
    CodeRedis(query.mobile, query.cate).set(code, ttl)
    # sms 发送验证码
    send_sms.delay(query.mobile, code, ttl)
    return {"message": "验证码发送成功"}
