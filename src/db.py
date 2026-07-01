from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ये नए ORM इंस्टेंस हैं जो पूरी ऐप में टेबल्स मैनेज करेंगे
db = SQLAlchemy()
migrate = Migrate()
