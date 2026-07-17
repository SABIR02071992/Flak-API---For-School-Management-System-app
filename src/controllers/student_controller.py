from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_jwt
from sqlalchemy import text
from src.extensions import db
from src.models.student_model import Student
import os
from werkzeug.utils import secure_filename


def create_student_logic():
    try:
        claims = get_jwt()
        tenant_schema = claims.get("schema_context")

        if not tenant_schema:
            return jsonify({
                "success": False,
                "message": "Invalid tenant schema."
            }), 400

        
        admission_no = request.form.get("admission_no")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        gender = request.form.get("gender")
        dob = request.form.get("dob")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        father_name = request.form.get("father_name")
        mother_name = request.form.get("mother_name")
        class_name = request.form.get("class_name")
        section = request.form.get("section")
        address = request.form.get("address")
        photo = request.files.get("photo")

        # ---------------------------------
        # Required Validation
        # ---------------------------------
        if not admission_no:
            return jsonify({
                "success": False,
                "message": "Admission Number is required."
            }), 400

        if not first_name:
            return jsonify({
                "success": False,
                "message": "First Name is required."
            }), 400

        if not class_name:
            return jsonify({
                "success": False,
                "message": "Class is required."
            }), 400

        if not section:
            return jsonify({
                "success": False,
                "message": "Section is required."
            }), 400

        # ---------------------------------
        # Change Search Path
        # ---------------------------------
        db.session.execute(
            text(f'SET search_path TO "{tenant_schema}"')
        )

        # ---------------------------------
        # Duplicate Admission Number
        # ---------------------------------
        existing_student = Student.query.filter_by(
            admission_no=admission_no
        ).first()

        if existing_student:
            return jsonify({
                "success": False,
                "message": "Admission Number already exists."
            }), 409

        # ---------------------------------
        # Generate Roll Number
        # Class + Section Wise
        # ---------------------------------
        last_student = (
            Student.query
            .filter_by(
                class_name=class_name,
                section=section
            )
            .order_by(Student.id.desc())
            .first()
        )

        if last_student and last_student.roll_no:
            roll_no = str(int(last_student.roll_no) + 1)
        else:
            roll_no = "1"

        # ---------------------------------
        # Convert DOB
        # ---------------------------------
        dob_obj = None

        if dob:
            try:
                dob_obj = datetime.strptime(
                    dob,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                return jsonify({
                    "success": False,
                    "message": "DOB format should be YYYY-MM-DD."
                }), 400

        # ---------------------------------
        # Create Student
        # ---------------------------------

        photo_path = None
        if photo:
            upload_folder = "uploads/students"
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(photo.filename)
            file_path = os.path.join(upload_folder, filename)
            photo.save(file_path)
            photo_path = file_path.replace("\\", "/")

        student = Student(
            admission_no=admission_no,
            roll_no=roll_no,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob_obj,
            mobile=mobile,
            email=email,
            father_name=father_name,
            mother_name=mother_name,
            class_name=class_name,
            section=section,
            address=address,
            photo=photo_path,
            status="active"
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Student created successfully.",
            "data": {
                "id": student.id,
                "admission_no": student.admission_no,
                "roll_no": student.roll_no,
                "student_name": f"{student.first_name} {student.last_name or ''}".strip(),
                "class": student.class_name,
                "section": student.section
            }
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
def get_all_students_logic():
    try:
        claims = get_jwt()
        tenant_schema = claims.get("schema_context")

        if not tenant_schema:
            return jsonify({
                "success": False,
                "message": "Invalid tenant schema."
            }), 400


        # Tenant schema set
        db.session.execute(
        text(f'SET search_path TO "{tenant_schema}"'))

        db.session.commit()
        students = db.session.execute(
            text(
                f'''
                SELECT *
                FROM "{tenant_schema}".students
                ORDER BY id DESC
                '''
            )
        ).mappings().all()

        student_list = []

        for student in students:
            student_list.append({
                "id": student.id,
                "admission_no": student.admission_no,
                "roll_no": student.roll_no,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "gender": student.gender,
                "dob": student.dob.strftime("%Y-%m-%d") if student.dob else None,
                "mobile": student.mobile,
                "email": student.email,
                "father_name": student.father_name,
                "mother_name": student.mother_name,
                "class_name": student.class_name,
                "section": student.section,
                "photo": student.photo,
                "status": student.status
            })


        return jsonify({
            "success": True,
            "count": len(student_list),
            "students": student_list
        }), 200


    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500