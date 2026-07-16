from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.controllers.user_controller import get_all_users_logic

get_users_bp = Blueprint("get_users_bp", __name__)

@get_users_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    return get_all_users_logic()