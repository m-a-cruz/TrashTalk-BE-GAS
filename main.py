import eventlet
eventlet.monkey_patch()
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import sys
from os.path import abspath, dirname
sys.path.append(abspath(dirname(__file__)))

from app.routes import auth, gas, insight, camera
from app.controller.camera import watch_changes
from app.management.middleware import log_request, protected_route
from extensions import socketio
from app.management.config import AppConfig
from scheduler import start_scheduler

# Initialize Flask App
app = Flask(__name__)
CORS(app, supports_credentials=True)

# SocketIO setup with eventlet
socketio.init_app(app)

# App Configs
app.config.update({
    "JWT_SECRET_KEY": AppConfig.JWT_SECRET_KEY,
    "JWT_TOKEN_LOCATION": AppConfig.JWT_TOKEN_LOCATION,
    "JWT_ACCESS_COOKIE_NAME": AppConfig.JWT_ACCESS_COOKIE_NAME,
    "JWT_COOKIE_CSRF_PROTECT": AppConfig.JWT_COOKIE_CSRF_PROTECT,
    "JWT_COOKIE_SECURE": AppConfig.JWT_COOKIE_SECURE,
    "MAIL_SERVER": AppConfig.MAIL_SERVER,
    "MAIL_PORT": AppConfig.MAIL_PORT,
    "MAIL_USE_TLS": AppConfig.MAIL_USE_TLS,
    "MAIL_USERNAME": AppConfig.MAIL_USERNAME,
    "MAIL_PASSWORD": AppConfig.MAIL_PASSWORD,
})

# Extensions
jwt = JWTManager(app)
mail = Mail(app)

# Middleware
@app.before_request
def before_request():
    log_request(request)

# Protected test route
@app.route("/protected", methods=["GET"])
@protected_route
def protected():
    return jsonify({"message": "You have access to this route!"}), 200

#
# Register blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(gas.gas_bp)
app.register_blueprint(insight.insight_bp)
app.register_blueprint(camera.camera_bp)

# Start the app with SocketIO
if __name__ == "__main__":
    start_scheduler()  # Enable if needed
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
