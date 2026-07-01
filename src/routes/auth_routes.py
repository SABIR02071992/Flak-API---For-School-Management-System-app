from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash  # Production standard password check
from src.db import db
from src.models.school_model import School  # Public context registry mapping

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # 🟢 CORRECTION 1: Role field ko hata diya gaya hai. Ab school_domain mandatory hai.
        if not data or 'email' not in data or 'password' not in data or 'school_domain' not in data:
            return jsonify({"error": "Missing fields: email, password, and school_domain are mandatory"}), 400
            
        email = data['email'].strip()
        password = data['password']
        school_domain = data['school_domain'].strip().lower()

        # Step 1: Central Registry se school ka custom schema name nikalna
        target_school = School.query.filter_by(domain=school_domain, status='active').first()
        if not target_school:
            return jsonify({"error": f"School/College with domain '{school_domain}' is not registered or active"}), 404

        tenant_schema = target_school.schema_name  # e.g., 'school_lbsh'

        # Step 2: Dynamic run-time lookup usi school schema ki users table ke andar
        # Isse user ka record aur uska actual 'role' bina frontend se bheje auto-detect ho jayega
        user_record = db.session.execute(db.text(f"""
            SELECT id, name, email, password_hash, role, status 
            FROM {tenant_schema}.users 
            WHERE email = :email LIMIT 1;
        """), {"email": email}).fetchone()

        # Verification block (Safe tuple mapping check)
        if user_record and check_password_hash(user_record.password_hash, password):
            
            # Check if user account is disabled by admin
            if user_record.status != 'active':
                return jsonify({"error": "Your account is currently inactive. Contact your administration."}), 403

            # 🟢 JWT Generation with Auto-Detected Role & School Meta
            access_token = create_access_token(
                identity=str(user_record.id), 
                additional_claims={
                    "role": user_record.role,           # Auto-detected (e.g., 'school-admin', 'Teacher')
                    "school_domain": school_domain,
                    "schema_context": tenant_schema
                }
            )
            
            # Flutter App ke liye optimized matching json callback
            return jsonify({
                "success": True,
                "message": "Login Successful!",
                "token": access_token,
                "user": {
                    "id": user_record.id,
                    "name": user_record.name,
                    "email": user_record.email,
                    "role": user_record.role,           # UI dynamic redirection ke liye zaroori hai
                    "school_name": target_school.name,  # Flutter dashboard Title me show karne ke liye
                    "school_domain": school_domain
                }
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": f"Internal Login Gateway Crash: {str(e)}"}), 500
