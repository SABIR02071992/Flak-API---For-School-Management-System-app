from flask import Blueprint
from src.controllers.class_controller import create_class_logic
from src.controllers.class_controller import get_all_classes_logic
from src.middleware.decorators import role_required

class_bp = Blueprint("class_bp", __name__)

@class_bp.route("/create", methods=["POST"])
@role_required([
    "super_admin",
    "School Admin",
    "Teacher"
])
def create_class():
    return create_class_logic()

# Get All Classes
@class_bp.route("/all", methods=["GET"])
@role_required([
    "super_admin",
    "School Admin",
    "Teacher"
])
def get_all_classes():
    return get_all_classes_logic()