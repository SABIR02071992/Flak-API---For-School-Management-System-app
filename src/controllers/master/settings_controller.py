from flask import jsonify
from flask_jwt_extended import jwt_required,get_jwt
from src.extensions import db
from src.models.school_model import School


@jwt_required()
def settings_home_logic():

    try:

        claims=get_jwt()

        schema=claims["schema_context"]

        domain=claims["school_domain"]


        school=School.query.filter_by(
            domain=domain
        ).first()


        user=db.session.execute(
            db.text(f"""
            SELECT
            id,
            name,
            email,
            role
            FROM {schema}.users
            WHERE id=:id
            """),
            {
                "id":int(claims["sub"])
            }
        ).fetchone()


        menus=[

            {

                "title":"School Profile",
                "icon":"business",
                "route":"school_profile"

            },

            {

                "title":"My Profile",
                "icon":"person",
                "route":"profile"

            },

            {

                "title":"Change Password",
                "icon":"lock",
                "route":"change_password"

            },

            {

                "title":"Logout",
                "icon":"logout",
                "route":"logout"

            }

        ]


        return jsonify({

            "success":True,

            "message":"Settings Loaded Successfully",

            "data":{

                "school":{

                    "name":school.name,

                    "domain":school.domain,

                    "logo":school.logo_path,

                    "plan":school.plan_setup

                },

                "profile":{

                    "id":user.id,

                    "name":user.name,

                    "email":user.email,

                    "role":user.role

                },

                "menus":menus

            }

        }),200


    except Exception as e:

        return jsonify({

            "success":False,

            "message":str(e)

        }),500