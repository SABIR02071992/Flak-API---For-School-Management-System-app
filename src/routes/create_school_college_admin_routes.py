
from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.controllers.super_admin_controller import create_school_college_admin_logic
from src.middleware.decorators import role_required

create_school_admin_bp = Blueprint(
    "create_school_admin",
    __name__,
)

create_school_admin_bp.route(
    "/create-school-admin",
    methods=["POST"],
)(
    jwt_required()(
        role_required([
            "super_admin",
            "School Admin",
            "Teacher",
        ])(
            create_school_college_admin_logic
        )
    )
)