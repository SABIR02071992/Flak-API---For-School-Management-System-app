from flask import Blueprint

from src.controllers.user_controller import get_all_users_for_super_admin
from src.middleware.decorators import role_required

super_admin_users_bp = Blueprint(
    "super_admin_users",
    __name__
)

@super_admin_users_bp.route(
    "/super-admin/users",
    methods=["GET"]
)
@role_required(["super_admin"])
def get_all_users():

    return get_all_users_for_super_admin()