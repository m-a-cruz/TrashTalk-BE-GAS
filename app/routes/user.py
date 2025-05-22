from flask import Blueprint
import app.controller.user as user
from app.management.middleware import handle_errors

user_bp = Blueprint('auth', __name__, url_prefix='/api/user')

@user_bp.route('/user', methods=['GET'], endpoint='get_user')
@handle_errors
def get_user(): return user.get_user()

@user_bp.route('/user', methods=['PUT'], endpoint='update_user')
@handle_errors
def login_user(): return user.update_user()

@user_bp.route('/user', methods=['DELETE'], endpoint='delete_user')
@handle_errors
def logout(): return user.delete_user()