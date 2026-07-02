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