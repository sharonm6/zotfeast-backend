from flask import Flask


def build_app():
    app = Flask(__name__)

    from routes import recommendation
    app.register_blueprint(recommendation)

    return app

app = build_app()

@app.route('/')
def home():
    return 'API for Zot Feast'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)