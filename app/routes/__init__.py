from .main import main_bp
from .auth import auth_bp
from .admin import admin_bp

# 蓝图列表
blueprints = [main_bp, auth_bp, admin_bp]
