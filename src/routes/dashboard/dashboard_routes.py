from flask import Blueprint
from src.controllers.dashboard_controller import dashboard_home_logic

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/home")
def dashboard_home():
    return dashboard_home_logic()