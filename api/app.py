from flask import Flask
from flask_cors import CORS
from routes import api_routes  # Importing routes

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}},supports_credentials=True)  # Allow frontend to call API
app.secret_key = "TRDEZ1210QWERTY"  # Set a secret key for session management

UPLOAD_FOLDER = "data/uploads"
# Ensure session works properly
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Register routes
app.register_blueprint(api_routes, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
