# src/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# 🗄️ डेटाबेस हैंडलर (ORM Instance) - यह पूरी ऐप में टेबल्स मैनेज करेगा
db = SQLAlchemy()

# 🔄 डेटाबेस माइग्रेशन टूल - टेबल में बदलावों को सिंक करने के लिए
migrate = Migrate()

# 🔒 टोकन बेस्ड सिक्योरिटी टूल - ऑथेंटिकेशन और रोल्स मैनेज करने के लिए
jwt = JWTManager()
