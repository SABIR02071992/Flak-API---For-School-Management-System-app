from src.extensions import db

class School(db.Model):
    __tablename__ = 'schools'
    __table_args__ = {'schema': 'public'} # Yeh table hamesha central public schema me rahega

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(50), unique=True, nullable=False)
    schema_name = db.Column(db.String(100), unique=True, nullable=False) 
    logo_path = db.Column(db.String(255), nullable=True)
    admin_email = db.Column(db.String(120), nullable=True)
    plan_setup = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='active')                  
    
    # 🟢 CORRECTION: SQLAlchemy 2.0 aur Postgres timestamp compatibility ke liye use karein db.func
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def getSchoolList(self):
        return {
            "id": self.id,
            "schoolName": self.name,
            "domain": self.domain,
            "schemaName": self.schema_name,
            "adminEmail": self.admin_email,
            "planSetup": self.plan_setup,
            "logoPath": self.logo_path,
            "status": self.status
        }
