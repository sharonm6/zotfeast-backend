from flask import Flask
from routes import recommendation

def build_app():
    app = Flask(__name__)

    app.register_blueprint(recommendation)

    return app

app = build_app()

@app.route('/')
def home():
    return 'Running...'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)