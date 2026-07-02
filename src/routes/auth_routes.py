# src/routes/auth_routes.py
from flask import Blueprint
from src.controllers.auth_controller import login_logic

# 1. ब्लूप्रिंट को बिना किसी प्रिफिक्स के साधारण तरीके से डिफाइन करें
auth_bp = Blueprint('auth', __name__)

# 2. एंडपॉइंट को सीधे कंट्रोलर के फंक्शन से मैप करें (सही तरीका)
auth_bp.route('/login', methods=['POST'])(login_logic)
