from src.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    admission_no = db.Column(db.String(50), unique=True, nullable=False)

    roll_no = db.Column(db.String(20), nullable=True)

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100))

    gender = db.Column(db.String(20))

    dob = db.Column(db.Date)

    mobile = db.Column(db.String(20))

    email = db.Column(db.String(120))

    father_name = db.Column(db.String(100))

    mother_name = db.Column(db.String(100))

    class_name = db.Column(db.String(30))

    section = db.Column(db.String(30))

    address = db.Column(db.Text)

    photo = db.Column(db.String(255))

    status = db.Column(db.String(20), default="active")

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )