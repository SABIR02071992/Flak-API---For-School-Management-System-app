from flask import request, jsonify
from flask_jwt_extended import get_jwt
from sqlalchemy import text

from src.extensions import db


def create_class_logic():
    try:
        claims = get_jwt()

        schema = claims.get("schema_context")
        user_id = claims.get("sub")

        if not schema:
            return jsonify({
                "success": False,
                "message": "Invalid tenant schema."
            }), 400

        data = request.get_json()

        class_name = data.get("class_name", "").strip()
        description = data.get("description", "").strip()

        if not class_name:
            return jsonify({
                "success": False,
                "message": "Class name is required."
            }), 400

        # ==============================
        # Ensure Classes Table Exists
        # ==============================

        db.session.execute(text(f"""
            CREATE TABLE IF NOT EXISTS "{schema}".classes (

                id SERIAL PRIMARY KEY,

                class_name VARCHAR(100) NOT NULL UNIQUE,

                description TEXT,

                status VARCHAR(20) DEFAULT 'active',

                created_by INTEGER,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        db.session.commit()

        # ==============================
        # Duplicate Check
        # ==============================

        existing = db.session.execute(
            text(f"""
                SELECT id
                FROM "{schema}".classes
                WHERE LOWER(class_name) = LOWER(:class_name)
            """),
            {
                "class_name": class_name
            }
        ).fetchone()

        if existing:
            return jsonify({
                "success": False,
                "message": "Class already exists."
            }), 409

        # ==============================
        # Insert Class
        # ==============================

        result = db.session.execute(
            text(f"""
                INSERT INTO "{schema}".classes
                (
                    class_name,
                    description,
                    created_by
                )
                VALUES
                (
                    :class_name,
                    :description,
                    :created_by
                )
                RETURNING
                    id,
                    class_name,
                    description,
                    status,
                    created_by,
                    created_at,
                    updated_at
            """),
            {
                "class_name": class_name,
                "description": description,
                "created_by": user_id
            }
        )

        new_class = result.fetchone()

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Class created successfully.",
            "data": {
                "id": new_class.id,
                "class_name": new_class.class_name,
                "description": new_class.description,
                "status": new_class.status,
                "created_by": new_class.created_by,
                "created_at": new_class.created_at.isoformat() if new_class.created_at else None,
                "updated_at": new_class.updated_at.isoformat() if new_class.updated_at else None,
            }
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


def get_all_classes_logic():
    try:
        claims = get_jwt()

        schema = claims.get("schema_context")

        if not schema:
            return jsonify({
                "success": False,
                "message": "Invalid tenant schema."
            }), 400

        classes = db.session.execute(
            text(f"""
                SELECT
                    id,
                    class_name,
                    description,
                    status,
                    created_by,
                    created_at,
                    updated_at
                FROM "{schema}".classes
                ORDER BY id DESC
            """)
        ).fetchall()

        data = []

        for item in classes:
            data.append({
                "id": item.id,
                "class_name": item.class_name,
                "description": item.description,
                "status": item.status,
                "created_by": item.created_by,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            })

        return jsonify({
            "success": True,
            "message": "Classes fetched successfully.",
            "data": data
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500