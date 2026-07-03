# src/routes/super_admin/create_school_college_admin_routes.py
from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.controllers.super_admin_controller import create_school_college_admin_logic
from src.middleware.decorators import role_required

create_school_admin_bp = Blueprint('create_school_admin', __name__) # प्रिफिक्स खाली रखें


# एंडपॉइंट मैपिंग: पहले JWT चेक होगा, फिर मिडिलवेयर चेक करेगा कि रोल 'super_admin' है या नहीं
create_school_admin_bp.route('/create-school-admin', methods=['POST'])(
    jwt_required()(
       role_required(["super_admin", "School Aadmin"])(create_school_college_admin_logic)
    )
)
