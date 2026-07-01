import os
from flask_jwt_extended import jwt_required, get_jwt 
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from src.db import db
from src.models.school_model import School  

create_school_admin_bp = Blueprint('create_school_admin', __name__, url_prefix='/api/v1')

@create_school_admin_bp.route('/create-school-admin', methods=['POST'])
@jwt_required()
def create_school_college_admin():
    try:
        # 1. Authorization check for Super Admin
        claims = get_jwt()
        if claims.get("role") != "super_admin":
            return jsonify({"error": "Access Denied! Only Super Admin can perform this action"}), 403
        
        # 2. Parse request payload
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON request payload"}), 400

        # Exact requested fields extraction
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        school_domain = data.get('school_domain')
        password = data.get('password')

        # 3. Mandatory Fields Validation
        if not all([name, email, mobile, school_domain, password]):
            return jsonify({"error": "All fields (name, email, mobile, school_domain, password) are mandatory"}), 400

        # 4. Fetch Schema Context from Public Schema using Domain Identifier
        target_school = School.query.filter_by(domain=school_domain, status='active').first()
        if not target_school:
            return jsonify({"error": f"Active school/college with domain '{school_domain}' does not exist"}), 404

        tenant_schema = target_school.schema_name 

        # 5. Isolate unique email constraint within target database schema
        user_exists = db.session.execute(db.text(f"""
            SELECT id FROM {tenant_schema}.users WHERE email = :email LIMIT 1;
        """), {"email": email}).fetchone()

        if user_exists:
            return jsonify({"error": f"Email '{email}' is already registered in {target_school.name}"}), 400

        # 6. Cryptography password generation & safe SQL execution
        hashed_password = generate_password_hash(password)
        
        db.session.execute(db.text(f"""
            INSERT INTO {tenant_schema}.users (name, email, mobile, password_hash, role, status)
            VALUES (:name, :email, :mobile, :password_hash, 'School Aadmin', 'active');
        """), {
            "name": name, 
            "email": email, 
            "mobile": mobile,
            "password_hash": hashed_password
        })
        db.session.commit()

        # 7. Flutter JSON formatted success callback
        return jsonify({
            "success": True,
            "message": f"School Admin successfully created under {target_school.name}",
            "admin": {
                "name": name,
                "email": email,
                "mobile": mobile,
                "role": "School Aadmin",
                "schoolName": target_school.name,
                "schemaContext": tenant_schema
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal Server Crash Error: {str(e)}"}), 500
