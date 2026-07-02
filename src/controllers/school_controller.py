# src/controllers/school_controller.py
import os
from flask import request, jsonify, current_app, send_from_directory
from flask_jwt_extended import get_jwt 
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from src.extensions import db  # 💡 db अब extensions से आएगा
from src.models.school_model import School

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def setup_school_multipart():
    try:
        claims = get_jwt()
        # रोल वेरिफिकेशन
        if claims.get("role") != "super_admin":
            return jsonify({"error": "Access Denied! Only Super Admin can onboard schools"}), 403
        
        school_name = request.form.get('schoolName')
        domain = request.form.get('domain')
        admin_email = request.form.get('adminEmail')
        plan_setup = request.form.get('planSetup')

        if not all([school_name, domain, admin_email, plan_setup]):
            return jsonify({"error": "All fields are mandatory"}), 400

        clean_domain = domain.replace('.', '_').lower().strip()
        base_schema_name = f"school_{clean_domain}"
        generated_schema_name = base_schema_name

        # 🟢 AUTO-COUNTER COLLISION PROTECTION
        counter = 1
        while True:
            existing_school = School.query.filter_by(schema_name=generated_schema_name).first()
            if not existing_school:
                break
            generated_schema_name = f"{base_schema_name}_{counter}"
            counter += 1

        # लोगो फाइल लॉजिक
        if 'logo' not in request.files:
            return jsonify({"error": "School logo image file is required"}), 400
        file = request.files['logo']
        if file.filename == '':
            return jsonify({"error": "No file stream selected"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(f"{generated_schema_name}_{file.filename}")
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            return jsonify({"error": "Invalid format! Only PNG, JPG, JPEG allowed"}), 400

        # डेटाबेस स्कीमा बनाना
        db.session.execute(db.text(f"CREATE SCHEMA IF NOT EXISTS {generated_schema_name};"))
        db.session.commit()

        # सेंट्रल रजिस्ट्री एंट्री
        new_school = School(
            name=school_name,
            domain=clean_domain if counter == 1 else f"{clean_domain}{counter-1}",
            schema_name=generated_schema_name,
            logo_path=file_path,
            admin_email=admin_email,
            plan_setup=plan_setup,
            status="active"
        )
        db.session.add(new_school)
        db.session.commit()
        db.session.refresh(new_school)

        # स्कीमा के अंदर यूजर्स टेबल बनाना
        db.session.execute(db.text(f"""
            CREATE TABLE IF NOT EXISTS {generated_schema_name}.users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        db.session.commit()

        # डिफ़ॉल्ट स्कूल एडमिन (Principal) जोड़ना
        hashed_password = generate_password_hash("Admin@123")
        db.session.execute(db.text(f"""
            INSERT INTO {generated_schema_name}.users (name, email, password_hash, role)
            VALUES ('School Principal', :email, :password, 'School Admin')
            ON CONFLICT (email) DO NOTHING;
        """), {"email": admin_email, "password": hashed_password})
        db.session.commit()

        return jsonify({
            "message": "School Onboarded with unique identifier successfully!",
            "school": new_school.getSchoolList()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal Server Crash Error: {str(e)}"}), 500

def get_schools():
    try:
        active_schools = School.query.filter_by(status='active').all()
        return jsonify({
            "success": True, 
            "schools": [school.getSchoolList() for school in active_schools]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def serve_school_logos(filename):
    root_uploads_path = os.path.join(os.getcwd(), "uploads")
    return send_from_directory(root_uploads_path, filename)
