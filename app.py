from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Optional: Check if .env loaded successfully
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

from src import create_app

app = create_app("development")

print("\n--- REGISTERED FLASK ROUTES ---")
for rule in app.url_map.iter_rules():
    print(f"Path: {rule.rule} -> Methods: {list(rule.methods)}")
print("-------------------------------\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# from dotenv import load_dotenv
# import os

# # Load .env file
# load_dotenv()

# # Check .env loaded
# print("DATABASE_URL:", os.getenv("DATABASE_URL"))

# from src import create_app
# from src.extensions import db
# from sqlalchemy import text


# app = create_app("development")


# # ==============================
# # PGCRYPTO TEST
# # ==============================
# with app.app_context():

#     try:
#         result = db.session.execute(
#             text("""
#                 SELECT extname, extnamespace::regnamespace
#                 FROM pg_extension
#                 WHERE extname='pgcrypto';
#             """)
#         )

#         print("\nPGCRYPTO EXTENSION:")
#         print(result.fetchall())


#         result = db.session.execute(
#             text("SELECT public.gen_salt('bf');")
#         )

#         print("\nGEN_SALT TEST:")
#         print(result.fetchone())


#     except Exception as e:
#         print("\nPGCRYPTO ERROR:")
#         print(e)



# print("\n--- REGISTERED FLASK ROUTES ---")
# for rule in app.url_map.iter_rules():
#     print(f"Path: {rule.rule} -> Methods: {list(rule.methods)}")
# print("-------------------------------\n")


# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",
#         port=5000,
#         debug=True
#     )