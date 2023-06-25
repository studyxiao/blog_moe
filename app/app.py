from flask import Blueprint, Flask

from app.core.log import Logger
from config import config

from .user.api import bp as user_bp

app = Flask(__name__)

Logger(app)
app.config.from_object(config)

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api_bp.register_blueprint(user_bp)

app.register_blueprint(api_bp)
