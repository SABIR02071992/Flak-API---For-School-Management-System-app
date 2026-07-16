from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.extensions import db


@jwt_required()
def academics_home_logic():
    try:

        claims = get_jwt()

        schema = claims["schema_context"]

        user = db.session.execute(
            db.text(f"""
                SELECT id,name,email,role
                FROM {schema}.users
                WHERE id=:id
            """),
            {
                "id": int(claims["sub"])
            }
        ).fetchone()

        # TODO
        # Future me ye tables use hongi
        #
        # classes
        # subjects
        # attendance
        # timetable
        # exams

        statistics = [

            {
                "id":1,
                "title":"Classes",
                "count":24,
                "icon":"class",
                "color":"#3B82F6",
                "route":"classes"
            },

            {
                "id":2,
                "title":"Subjects",
                "count":72,
                "icon":"menu_book",
                "color":"#22C55E",
                "route":"subjects"
            },

            {
                "id":3,
                "title":"Attendance",
                "count":"96%",
                "icon":"fact_check",
                "color":"#F59E0B",
                "route":"attendance"
            },

            {
                "id":4,
                "title":"Exams",
                "count":8,
                "icon":"quiz",
                "color":"#8B5CF6",
                "route":"exams"
            }

        ]


        quick_actions = [

            {
                "title":"Classes",
                "icon":"class",
                "route":"classes"
            },

            {
                "title":"Subjects",
                "icon":"menu_book",
                "route":"subjects"
            },

            {
                "title":"Attendance",
                "icon":"fact_check",
                "route":"attendance"
            },

            {
                "title":"Timetable",
                "icon":"schedule",
                "route":"timetable"
            }

        ]


        today_classes = [

            {
                "class":"10-A",
                "subject":"Mathematics",
                "teacher":"Rahul Sharma",
                "time":"09:00 AM"
            },

            {
                "class":"9-B",
                "subject":"Science",
                "teacher":"Amit Kumar",
                "time":"10:30 AM"
            }

        ]


        return jsonify({

            "success":True,

            "message":"Academics Loaded Successfully",

            "data":{

                "user":{

                    "id":user.id,
                    "name":user.name,
                    "email":user.email,
                    "role":user.role

                },

                "statistics":statistics,

                "quick_actions":quick_actions,

                "today_classes":today_classes

            }

        }),200

    except Exception as e:

        return jsonify({

            "success":False,

            "message":str(e)

        }),500