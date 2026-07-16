# src/routes/__init__.py
from src.routes.auth_routes import auth_bp
from src.routes.school_routes import school_bp
from src.routes.super_admin_login_routes import super_admin_bp
from src.routes.create_school_college_admin_routes import create_school_admin_bp 
from .dashboard.dashboard_routes import dashboard_bp
from src.routes.master.people_routes import people_bp
from src.routes.master.academics_routes import academics_bp
from src.routes.master.settings_routes import settings_bp
from .student_routes import student_bp
from .class_routes import class_bp

__all__ = [
    'auth_bp',
    'school_bp', 
    'super_admin_bp', 
    'create_school_admin_bp', 
    'dashboard_bp', 
    'people_bp', 
    'academics_bp', 
    'settings_bp', 
    'student_bp',
    'class_bp'
    ]
