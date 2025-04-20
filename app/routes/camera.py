from flask import Blueprint
from app.controller import camera
from app.management.middleware import handle_errors, protected_route

camera_bp = Blueprint('camera', __name__, url_prefix='/api/camera')

@camera_bp.route('/latest', methods=['GET'], endpoint='view_latest_image')
@protected_route
@handle_errors
def view_latest_image(): return camera.view_latest_image()