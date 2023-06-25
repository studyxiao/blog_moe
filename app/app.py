from flask import Blueprint, Flask

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

# 路由
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api_bp.register_blueprint(user_bp)

app.register_blueprint(api_bp)
