from flask import Flask
from flask_cors import CORS
from routes import api_routes  # Importing routes

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow frontend to call API

# Register routes
app.register_blueprint(api_routes, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
