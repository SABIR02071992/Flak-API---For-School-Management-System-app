from src.extensions import db


class AppModule(db.Model):
    __tablename__ = "app_modules"
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer, primary_key=True)

    module_type = db.Column(db.String(50), nullable=False)

    title = db.Column(db.String(100), nullable=False)

    subtitle = db.Column(db.String(200))

    icon = db.Column(db.String(50), nullable=False)

    route = db.Column(db.String(100), nullable=False)

    color = db.Column(db.String(20))

    display_order = db.Column(db.Integer, default=1)

    is_active = db.Column(db.Boolean, default=True)