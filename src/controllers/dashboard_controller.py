from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.extensions import db


@jwt_required()
def dashboard_home_logic():
    try:
        # JWT Claims
        claims = get_jwt()

        schema = claims["schema_context"]
        role = claims["role"]

        # Logged in User
        user = db.session.execute(
            db.text(f"""
                SELECT id, name, email
                FROM {schema}.users
                WHERE id = :user_id
            """),
            {"user_id": int(claims["sub"])}
        ).fetchone()

        # Dashboard Statistics
        statistics = db.session.execute(
            db.text(f"""
                SELECT role, COUNT(*) AS total
                FROM {schema}.users
                WHERE status = 'active'
                GROUP BY role
            """)
        ).fetchall()

        counts = {
            "School Admin": 0,
            "Teacher": 0,
            "Student": 0,
            "Parent": 0
        }

        for row in statistics:
            counts[row.role] = row.total

        # Overview Cards
        overview = [
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

        # Quick Actions
        quick_actions = [
            {
                "id": 1,
                "title": "Students",
                "icon": "school",
                "color": "#3B82F6",
                "route": "students"
            },
            {
                "id": 2,
                "title": "Teachers",
                "icon": "person",
                "color": "#22C55E",
                "route": "teachers"
            },
            {
                "id": 3,
                "title": "Attendance",
                "icon": "fact_check",
                "color": "#F59E0B",
                "route": "attendance"
            },
            {
                "id": 4,
                "title": "Notice Board",
                "icon": "campaign",
                "color": "#EF4444",
                "route": "notice"
            }
        ]

        # Recent Activities
        recent_activities = [
            {
                "id": 1,
                "title": "New Student Registered",
                "subtitle": "Today • 10:30 AM",
                "icon": "person_add"
            }
        ]

        # Upcoming Events
        upcoming_events = []

        return jsonify({
            "success": True,
            "message": "Dashboard Loaded Successfully",
            "data": {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": role,
                    "school_domain": claims["school_domain"]
                },
                "overview": overview,
                "quick_actions": quick_actions,
                "recent_activities": recent_activities,
                "upcoming_events": upcoming_events
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500