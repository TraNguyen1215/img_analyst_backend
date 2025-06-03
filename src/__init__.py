from flask import Flask
from dotenv import load_dotenv

def create_app():
    # Load các biến môi trường từ tệp .env
    load_dotenv()

    # Khởi tạo ứng dụng Flask
    app = Flask(__name__)

    # Đăng ký các blueprint cho các module API
    from .api.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    from .api.histories import histories_bp
    app.register_blueprint(histories_bp, url_prefix='/api/histories')
    
    from .api.diease import diease_bp
    app.register_blueprint(diease_bp, url_prefix='/api/diease')
    
    from .api.material import material_bp
    app.register_blueprint(material_bp, url_prefix='/api/material')


    # Trả về ứng dụng Flask đã được cấu hình
    return app
