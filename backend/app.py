from flask import Flask
from flask_cors import CORS
from utils.security import hash_password, check_password
from neo4j_db import get_all_intents, update_answer, get_all_accounts, driver
from routes.intent_routes import intent_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Đăng ký các Blueprint
app.register_blueprint(intent_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
