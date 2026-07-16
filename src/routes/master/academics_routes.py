from flask import Blueprint

from src.controllers.master.academics_controller import academics_home_logic

academics_bp = Blueprint(
    "academics_bp",
    __name__,
)

academics_bp.route(
    "/academics",
    methods=["GET"]
)(academics_home_logic)