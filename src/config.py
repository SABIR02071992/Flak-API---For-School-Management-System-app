# src/config.py
import os
from datetime import timedelta

class Config:
    # .env से पढ़ें या डिफ़ॉल्ट पर सेट करें
    SECRET_KEY = os.getenv('SECRET_KEY') or 'super-secret-key-for-jwt'
    JWT_SECRET_KEY = os.getenv('SECRET_KEY') or 'super-secret-key-for-jwt'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 🟢 Token duration 1 Day
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1) 
    
    # DB Connection Pooling सेटिंग्स
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }
    
    UPLOAD_FOLDER = 'uploads/logos'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
