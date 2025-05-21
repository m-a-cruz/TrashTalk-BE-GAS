from flask import Blueprint
from app.controller import gas, notification
from app.management.middleware import handle_errors, protected_route

gas_bp = Blueprint('gas', __name__, url_prefix='/api/gas')

@gas_bp.route('/data', methods=['POST'], endpoint='create_gas_records')
@handle_errors
def create_gas_records(): return gas.record_gas_level()

@gas_bp.route('/charts', methods=['GET'], endpoint='get_gas_chart')
@protected_route
@handle_errors
def get_gas_chart(): return gas.fetch_gas_chart()

@gas_bp.route('/notification', methods=['POST'], endpoint='create_notification')
@handle_errors
def create_notification(): return notification.record_notif_data()

@gas_bp.route('/notifications', methods=['GET'], endpoint='get_notifications')
@protected_route
@handle_errors
def get_notifications(): return notification.fetch_notif()

@gas_bp.route('/notification', methods=['DELETE'], endpoint='delete_notification')
@handle_errors
def delete_notification(): return notification.delete_notif()

@gas_bp.route('/notification', methods=['PUT'], endpoint='update_notification')
@handle_errors
def update_notification(): return notification.update_notif_data()
