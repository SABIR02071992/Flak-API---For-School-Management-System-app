from flask import Blueprint

from src.controllers.master.people_controller import people_home_logic

people_bp = Blueprint("people_bp",__name__,)

people_bp.route("/people", methods=["GET"])(people_home_logic)