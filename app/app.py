from flask import Blueprint, Flask
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import HTTPException

from app.core.exception import APIException
from app.core.log import Logger
from app.core.model import db
from config import config

from .user.api import bp as user_bp

app = Flask(__name__)

# 配置项
app.config.from_object(config)

# 插件
Logger(app)
db.init_app(app)


def error_handler_http(error: HTTPException) -> ResponseReturnValue:
    return APIException(error.code, error.code, error.description)


app.register_error_handler(HTTPException, error_handler_http)

# 路由
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api_bp.register_blueprint(user_bp)

app.register_blueprint(api_bp)
