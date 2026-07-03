from werkzeug.security import check_password_hash
from src.extensions import db


class SuperAdmin(db.Model):
    __tablename__ = 'super_admins'
    __table_args__ = {'schema': 'public'} # Yeh central public schema me rahega

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Note: Kyunki aapne Postgres ke crypt() se hash kiya hai, isliye length 255 rakhein
    password_hash = db.Column(db.String(255), nullable=False) 