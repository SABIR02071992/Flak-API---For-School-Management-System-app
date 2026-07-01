from src import create_app

# हमारी नई Application Factory से ऐप लोड करें
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
