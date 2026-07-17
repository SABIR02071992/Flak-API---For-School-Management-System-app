# src/controllers/super_admin_controller.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt
from werkzeug.security import generate_password_hash
from src.extensions import db
from src.models.school_model import School


def super_admin_login_logic():
    """Super Admin Login Logic"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON request payload"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        

        # query = """
        #     SELECT id, name, email
        #     FROM public.super_admins
        #     WHERE email = :email
        #       AND password_hash = crypt(:password, password_hash);
        # """
        query = """
            SELECT id, name, email
            FROM public.super_admins
            WHERE email = :email
            AND password_hash = public.crypt(
            CAST(:password AS TEXT),
            CAST(password_hash AS TEXT)
            );
        """

        result = db.session.execute(
            db.text(query),
            {
                "email": email,
                "password": password,
            },
        ).fetchone()

        if result is None:
            return jsonify({"error": "Invalid Email or Password"}), 401

        access_token = create_access_token(
            identity=str(result[0]),
            additional_claims={"role": "super_admin"},
        )

        return jsonify(
            {
                "success": True,
                "message": "Super Admin Login Successful!",
                "token": access_token,
                "user": {
                    "id": result[0],
                    "name": result[1],
                    "email": result[2],
                    "role": "super_admin",
                },
            }
        ), 200

    except Exception as e:
        return jsonify(
            {"error": f"Internal Server Login Error: {str(e)}"}
        ), 500


def create_school_college_admin_logic():
    """Create User Logic"""

    try:
        # Logged-in User Role
        claims = get_jwt()
        logged_in_role = claims.get("role")

        # Request Body
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing JSON request payload"}), 400

        name = data.get("name")
        email = data.get("email")
        mobile = data.get("mobile")
        school_domain = data.get("school_domain")
        password = data.get("password")
        role = data.get("role")

        # Mandatory Validation
        if not all([name, email, mobile, school_domain, password, role]):
            return jsonify(
                {
                    "error": "All fields (name, email, mobile, school_domain, password, role) are mandatory"
                }
            ), 400

        # ==========================================================
        # ROLE PERMISSION MATRIX
        # ==========================================================

        role_permissions = {
            "super_admin": [
                "School Admin",
                "Teacher",
                "Student",
                "Parent",
            ],

            "School Admin": [
                "Teacher",
                "Student",
                "Parent",
            ],

            "Teacher": [
                "Student",
                "Parent",
            ],
        }

        allowed_roles = role_permissions.get(logged_in_role)

        if allowed_roles is None:
            return jsonify(
                {
                    "error": "You are not authorized to create users."
                }
            ), 403

        if role not in allowed_roles:
            return jsonify(
                {
                    "error": f"'{logged_in_role}' cannot create '{role}' users."
                }
            ), 403

        # ==========================================================
        # Fetch School
        # ==========================================================

        target_school = School.query.filter_by(
            domain=school_domain,
            status="active",
        ).first()

        if not target_school:
            return jsonify(
                {
                    "error": f"Active school/college with domain '{school_domain}' does not exist"
                }
            ), 404

        tenant_schema = target_school.schema_name

        # ==========================================================
        # Duplicate Email Check
        # ==========================================================

        user_exists = db.session.execute(
            db.text(
                f"""
                SELECT id
                FROM {tenant_schema}.users
                WHERE email = :email
                LIMIT 1;
                """
            ),
            {"email": email},
        ).fetchone()

        if user_exists:
            return jsonify(
                {
                    "error": f"Email '{email}' is already registered in {target_school.name}"
                }
            ), 400

        # ==========================================================
        # Password Hash
        # ==========================================================

        hashed_password = generate_password_hash(password)

        # ==========================================================
        # Insert User
        # ==========================================================

        db.session.execute(
            db.text(
                f"""
                INSERT INTO {tenant_schema}.users
                (
                    name,
                    email,
                    mobile,
                    password_hash,
                    role,
                    status
                )
                VALUES
                (
                    :name,
                    :email,
                    :mobile,
                    :password_hash,
                    :role,
                    'active'
                );
                """
            ),
            {
                "name": name,
                "email": email,
                "mobile": mobile,
                "password_hash": hashed_password,
                "role": role,
            },
        )

        db.session.commit()

        # ==========================================================
        # Success Response
        # ==========================================================

        return jsonify(
            {
                "success": True,
                "message": f"{role} created successfully under {target_school.name}",
                "user": {
                    "name": name,
                    "email": email,
                    "mobile": mobile,
                    "role": role,
                    "schoolName": target_school.name,
                    "schemaContext": tenant_schema,
                },
            }
        ), 201

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {
                "error": f"Internal Server Crash Error: {str(e)}"
            }
        ), 500