# src/routes/super_admin_login_routes.py
from flask import Blueprint
from src.controllers.super_admin_controller import super_admin_login_logic

# सुनिश्चित करें कि वेरिएबल का नाम बिल्कुल यही हो (small letters में)
super_admin_bp = Blueprint('super_admin', __name__) # प्रिफिक्स खाली रखें

super_admin_bp.route('/login', methods=['POST'])(super_admin_login_logic)
