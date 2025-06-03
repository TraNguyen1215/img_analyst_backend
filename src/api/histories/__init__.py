from flask import Blueprint

# Khởi tạo blueprint cho monitoring well
histories_bp = Blueprint('histories', __name__)

from . import routes