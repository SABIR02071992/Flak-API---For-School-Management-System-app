# from src import create_app

# # हमारी नई Application Factory से ऐप लोड करें
# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# app.py (F:\Dev-Sabir\Flask APIs\app.py)
from src import create_app

app = create_app('development')

# 🔍 यह कोड टर्मिनल में प्रिंट करेगा कि आपकी असल में कौन-कौन सी APIs बनी हैं
print("\n--- REGISTERED FLASK ROUTES ---")
for rule in app.url_map.iter_rules():
    print(f"Path: {rule.rule} -> Methods: {list(rule.methods)}")
print("-------------------------------\n")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
