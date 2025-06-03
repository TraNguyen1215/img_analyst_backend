from flask import Blueprint

# Khởi tạo blueprint cho monitoring well
material_bp = Blueprint('material', __name__)

from . import routes