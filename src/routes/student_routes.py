from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.middleware.decorators import role_required
from src.controllers.student_controller import (
    create_student_logic,
    get_all_students_logic
)

student_bp = Blueprint("student", __name__)

# ==============================
# Create Student
# ==============================
@student_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["School Admin", "Teacher"])
def create_student():
    return create_student_logic()

# ==============================
# Get All Students
# ==============================
@student_bp.route("/all", methods=["GET"])
@jwt_required()
@role_required(["School Admin", "Teacher"])
def get_all_students():
    return get_all_students_logic()