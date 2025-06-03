from flask import Blueprint

# Khởi tạo blueprint cho monitoring well
diease_bp = Blueprint('diease', __name__)

from . import routes