
# src/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src.extensions import db, migrate, jwt 
from src.config import config_by_name
from src.routes.users.get_users_routes import get_users_bp
from src.routes.users.get_all_users_routes import super_admin_users_bp
from src.routes.student_routes import student_bp

# .env फ़ाइल लोड करें
load_dotenv()

def create_app(config_name='development'):
    app = Flask(__name__)

    # ⚙️ config.py से सभी सेटिंग्स एक साथ लोड करें
    app.config.from_object(config_by_name[config_name])

    # Flutter web और mobile के लिए CORS इनेबल करें
    CORS(app)

    # Logos सेव करने के लिए अपलोड फोल्डर सेट करें
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 🔌 एक्सटेंशन्स को ऐप के साथ इनिशियलाइज़ करें
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # 🗄️ Models को Lazily इम्पोर्ट करें ताकि SQLAlchemy डिटेक्ट कर सके
    with app.app_context():
        from src import models

    # 🛣️ Saare Blueprints को इम्पोर्ट और रजिस्टर करें
    #from src.routes import auth_bp, school_bp, super_admin_bp, create_school_admin_bp, dashboard_bp, people_bp, academics_bp, settings_bp, student_bp,
    from src.routes import (
    auth_bp,
    school_bp,
    super_admin_bp,
    create_school_admin_bp,
    dashboard_bp,
    people_bp,
    academics_bp,
    settings_bp,
    student_bp,
    class_bp,
    ) 
    
    # 🛣️ Saare Blueprints ko sahi url_prefix ke sath register karein
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(school_bp, url_prefix='/api/v1/school')
    app.register_blueprint(super_admin_bp, url_prefix='/api/v1/super-admin')
    app.register_blueprint(create_school_admin_bp, url_prefix='/api/v1')
    app.register_blueprint(get_users_bp,url_prefix='/api/v1')
    app.register_blueprint(super_admin_users_bp, url_prefix="/api/v1")
    app.register_blueprint(dashboard_bp,url_prefix="/api/v1/dashboard")
    app.register_blueprint(people_bp,url_prefix="/api/v1/master",)
    app.register_blueprint(academics_bp,url_prefix="/api/v1/master")
    app.register_blueprint(settings_bp,url_prefix="/api/v1/master")
    app.register_blueprint(student_bp,url_prefix="/api/v1/student")
    app.register_blueprint(class_bp,url_prefix="/api/v1/class",)


    return app
