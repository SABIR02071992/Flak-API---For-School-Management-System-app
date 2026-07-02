# src/controllers/auth_controller.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from src.extensions import db  # 💡 ध्यान दें: db अब extensions से आएगा
from src.models.school_model import School

def login_logic():
    try:
        data = request.get_json()
        
        # वैलीडेशन चेक
        if not data or 'email' not in data or 'password' not in data or 'school_domain' not in data:
            return jsonify({"error": "Missing fields: email, password, and school_domain are mandatory"}), 400
            
        email = data['email'].strip()
        password = data['password']
        school_domain = data['school_domain'].strip().lower()

        # Step 1: Central Registry से स्कूल चेक करना
        target_school = School.query.filter_by(domain=school_domain, status='active').first()
        if not target_school:
            return jsonify({"error": f"School/College with domain '{school_domain}' is not registered or active"}), 404

        tenant_schema = target_school.schema_name

        # Step 2: डायनेमिक स्कीमा लुकअप
        user_record = db.session.execute(db.text(f"""
            SELECT id, name, email, password_hash, role, status 
            FROM {tenant_schema}.users 
            WHERE email = :email LIMIT 1;
        """), {"email": email}).fetchone()

        # पासवर्ड और स्टेटस वेरिफिकेशन
        if user_record and check_password_hash(user_record.password_hash, password):
            
            if user_record.status != 'active':
                return jsonify({"error": "Your account is currently inactive. Contact your administration."}), 403

            # JWT टोकन जनरेशन
            access_token = create_access_token(
                identity=str(user_record.id), 
                additional_claims={
                    "role": user_record.role,
                    "school_domain": school_domain,
                    "schema_context": tenant_schema
                }
            )
            
            return jsonify({
                "success": True,
                "message": "Login Successful!",
                "token": access_token,
                "user": {
                    "id": user_record.id,
                    "name": user_record.name,
                    "email": user_record.email,
                    "role": user_record.role,
                    "school_name": target_school.name,
                    "school_domain": school_domain
                }
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": f"Internal Login Gateway Crash: {str(e)}"}), 500
