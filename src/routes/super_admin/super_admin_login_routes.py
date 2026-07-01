from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token # Real token generator
from src.db import db

super_admin_bp = Blueprint('super_admin', __name__, url_prefix='/api/v1/super-admin')

@super_admin_bp.route('/login', methods=['POST'])
def super_admin_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        query = """
            SELECT id, name, email FROM public.super_admins 
            WHERE email = :email AND password_hash = crypt(:password, password_hash);
        """
        result = db.session.execute(db.text(query), {"email": email, "password": password}).fetchone()

        if result is None:
            return jsonify({"error": "Invalid Email or Password"}), 401

        # 🚀 REAL JWT TOKEN: Isme user id aur custom role 'super_admin' encode kiya gaya hai
        access_token = create_access_token(identity=str(result[0]), additional_claims={"role": "super_admin"})

        return jsonify({
            "success": True,
            "message": "Super Admin Login Successful!",
            "token": access_token,
            "user": {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "role": "super_admin"
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Login Error: {str(e)}"}), 500
