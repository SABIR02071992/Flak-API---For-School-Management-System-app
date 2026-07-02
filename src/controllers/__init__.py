# src/controllers/__init__.py
from src.controllers.auth_controller import login_logic
from src.controllers.school_controller import setup_school_multipart, get_schools, serve_school_logos
from src.controllers.super_admin_controller import super_admin_login_logic, create_school_college_admin_logic

# सभी महत्वपूर्ण फंक्शन्स को आसानी से एक्सपोर्ट करने के लिए
__all__ = [
    'login_logic',
    'setup_school_multipart',
    'get_schools',
    'serve_school_logos',
    'super_admin_login_logic',
    'create_school_college_admin_logic'
]
