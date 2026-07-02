# src/controllers/super_admin_controller.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt
from werkzeug.security import generate_password_hash
from src.extensions import db  # db अब extensions.py से इम्पोर्ट हो रहा है
from src.models.school_model import School

def super_admin_login_logic():
    """1. सुपर एडमिन लॉगिन लॉजिक (PostgreSQL crypt() आधारित)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON request payload"}), 400
            
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # PostgreSQL crypt() के ज़रिए पासवर्ड मैच करने की क्वेरी
        query = """
            SELECT id, name, email FROM public.super_admins 
            WHERE email = :email AND password_hash = crypt(:password, password_hash);
        """
        result = db.session.execute(db.text(query), {"email": email, "password": password}).fetchone()

        if result is None:
            return jsonify({"error": "Invalid Email or Password"}), 401

        # रियल JWT टोकन जनरेशन (सुपर एडमिन रोल के साथ)
        access_token = create_access_token(
            identity=str(result[0]), 
            additional_claims={"role": "super_admin"}
        )

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


def create_school_college_admin_logic():
    """2. 🆕 नया स्कूल एडमिन क्रिएशन लॉजिक (मल्टी-टेनेंट स्कीमा आधारित)"""
    try:
        # 1. Authorization check for Super Admin
        claims = get_jwt()
        if claims.get("role") != "super_admin":
            return jsonify({"error": "Access Denied! Only Super Admin can perform this action"}), 403
        
        # 2. Parse request payload
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON request payload"}), 400

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
        
        # मोबाइल कॉलम को इन्सर्ट क्वेरी में शामिल किया गया है
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
