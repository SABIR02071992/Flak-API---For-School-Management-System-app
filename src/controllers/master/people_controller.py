from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.extensions import db


@jwt_required()
def people_home_logic():
    try:
        claims = get_jwt()

        schema = claims["schema_context"]

        # ----------------------------
        # Logged In User
        # ----------------------------
        user = db.session.execute(
            db.text(f"""
                SELECT id,name,email,role
                FROM {schema}.users
                WHERE id=:user_id
            """),
            {
                "user_id": int(claims["sub"])
            }
        ).fetchone()

        # ----------------------------
        # Statistics
        # ----------------------------
        result = db.session.execute(
            db.text(f"""
                SELECT role,COUNT(*) total
                FROM {schema}.users
                WHERE status='active'
                GROUP BY role
            """)
        ).fetchall()

        counts = {
            "Student": 0,
            "Teacher": 0,
            "Parent": 0,
            "School Admin": 0
        }

        for row in result:
            counts[row.role] = row.total

        statistics = [
            {
                "id": 1,
                "title": "Students",
                "count": counts["Student"],
                "icon": "school",
                "color": "#3B82F6",
                "route": "students"
            },
            {
                "id": 2,
                "title": "Teachers",
                "count": counts["Teacher"],
                "icon": "person",
                "color": "#22C55E",
                "route": "teachers"
            },
            {
                "id": 3,
                "title": "Parents",
                "count": counts["Parent"],
                "icon": "groups",
                "color": "#8B5CF6",
                "route": "parents"
            },
            {
                "id": 4,
                "title": "School Admins",
                "count": counts["School Admin"],
                "icon": "admin_panel_settings",
                "color": "#F59E0B",
                "route": "school_admins"
            }
        ]

        # ----------------------------
        # Recent Joined Users
        # ----------------------------

        recent = db.session.execute(
            db.text(f"""
                SELECT
                    id,
                    name,
                    role,
                    created_at
                FROM {schema}.users
                ORDER BY created_at DESC
                LIMIT 10
            """)
        ).fetchall()

        recent_joined = []

        for row in recent:
            recent_joined.append({
                "id": row.id,
                "name": row.name,
                "role": row.role,
                "created_at": row.created_at.strftime("%d %b %Y")
            })

        return jsonify({

            "success": True,

            "message": "People Loaded Successfully",

            "data": {

                "user": {

                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role

                },

                "statistics": statistics,

                "recent_joined": recent_joined

            }

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500