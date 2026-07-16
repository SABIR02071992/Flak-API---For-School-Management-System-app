from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.controllers.student_controller import create_student_logic
from src.middleware.decorators import role_required

student_bp = Blueprint("student", __name__)


@student_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required(["School Admin", "Teacher"])
def create_student():
    return create_student_logic()