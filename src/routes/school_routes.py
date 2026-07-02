# src/routes/school_routes.py
from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.controllers.school_controller import (
    setup_school_multipart, 
    get_schools, 
    serve_school_logos
)

school_bp = Blueprint('school', __name__) # प्रिफिक्स खाली रखें


# 🛣️ एंडपॉइंट्स मैपिंग
school_bp.route('/setup', methods=['POST'])(jwt_required()(setup_school_multipart))
school_bp.route('/list', methods=['GET'])(get_schools)
school_bp.route('/uploads/<path:filename>', methods=['GET'])(serve_school_logos)
