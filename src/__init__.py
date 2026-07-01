import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS # Flutter web aur mobile connections ke liye zaroori hai
from dotenv import load_dotenv
from src.db import db, migrate
from datetime import timedelta

# .env फ़ाइल लोड करें
load_dotenv()

def create_app():
    app = Flask(__name__)

    # CORS settings enabled ki taki local network device se hit karne par error na aaye
    CORS(app)

    # .env से DATABASE_URL पढ़ें, नहीं तो सीधे आपके Neon DB से कनेक्ट करें
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or "postgresql://neondb_owner:npg_UpeHSjEu9gx4@ep-dark-star-ah3akqx1-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'super-secret-key-for-jwt'
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY') or 'super-secret-key-for-jwt'

     # 🟢 CORRECTION 2: Token duration badha kar 1 Days kiya (Baar-baar session timeout nahi hoga)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) 
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }

    # Logos save karne ke liye upload folder setup
    UPLOAD_FOLDER = 'uploads/logos'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Database aur Migration initialize karein
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # 🟢 1. Models ko lazily import karein taki SQLAlchemy unhe auto-detect kar sake
    with app.app_context():
        from src import models

    # 🟢 2. Package `src.routes` se saare blueprints ek baar me import karein
    from src.routes import auth_bp, school_bp, super_admin_bp, create_school_admin_bp
    
    # 🟢 3. Saare blueprints ko app context me register karein
    app.register_blueprint(auth_bp)
    app.register_blueprint(school_bp)
    app.register_blueprint(super_admin_bp) # Super Admin login API active hui
    app.register_blueprint(create_school_admin_bp)

    return app
