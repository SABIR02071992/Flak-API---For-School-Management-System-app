# src/routes/__init__.py
from src.routes.auth_routes import auth_bp
from src.routes.school_routes import school_bp
from src.routes.super_admin_login_routes import super_admin_bp
from src.routes.create_school_college_admin_routes import create_school_admin_bp 

__all__ = ['auth_bp', 'school_bp', 'super_admin_bp', 'create_school_admin_bp']
