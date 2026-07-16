from flask import Blueprint

from src.controllers.master.settings_controller import settings_home_logic

settings_bp=Blueprint(
    "settings_bp",
    __name__,
)

settings_bp.route(
    "/settings",
    methods=["GET"]
)(settings_home_logic)