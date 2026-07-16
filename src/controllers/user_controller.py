from flask import jsonify
from flask_jwt_extended import get_jwt
from sqlalchemy import text

from src.extensions import db
from src.models.school_model import School


def get_all_users_logic():
    try:
        # JWT se school domain nikalo
        claims = get_jwt()
        school_domain = claims.get("school_domain")

        if not school_domain:
            return jsonify({
                "error": "School domain not found in token."
            }), 400

        # Public schema se school details nikalo
        school = School.query.filter_by(domain=school_domain).first()

        if not school:
            return jsonify({
                "error": "School not found."
            }), 404

        schema_name = school.schema_name

        # Users fetch
        query = text(f"""
            SELECT
                id,
                name,
                email,
                role,
                status,
                created_at
            FROM "{schema_name}".users
            ORDER BY id ASC;
        """)

        result = db.session.execute(query)

        users = []

        for row in result.mappings():
            users.append({
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "role": row["role"],
                "status": row["status"],
                "created_at": str(row["created_at"])
            })

        return jsonify({
            "success": True,
            "total_users": len(users),
            "users": users
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
def get_all_users_for_super_admin():
    """
    Super Admin:
    Fetch all users from every school's schema.
    """

    try:
        schools = School.query.all()
        all_users = []
        for school in schools:
            schema_name = school.schema_name
            query = text(f"""
                SELECT
                    id,
                    name,
                    email,
                    role,
                    status,
                    created_at
                FROM "{schema_name}".users
                ORDER BY id DESC
            """)

            result = db.session.execute(query)

            for row in result.mappings():

                all_users.append({
                    "id": row["id"],
                    "name": row["name"],
                    "email": row["email"],
                    "role": row["role"],
                    "status": row["status"],
                    "created_at": str(row["created_at"]),
                    "school_name": school.name,
                    "school_domain": school.domain
                })

        return jsonify({
            "success": True,
            "total_users": len(all_users),
            "users": all_users
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500