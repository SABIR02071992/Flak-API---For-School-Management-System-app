from src.extensions import db


class SchoolClass(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)

    class_name = db.Column(db.String(100), nullable=False, unique=True)

    status = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "status": self.status,
        }