from services.Driver.driver_service import get_driver_usterki_service
from utils.driver_utilis import driver_required
from flask import Blueprint, jsonify, g
from utils.jwt_utils import token_required

drivers_bp = Blueprint('drivers_bp', __name__)

@drivers_bp.route('/api/driver/usterki', methods=['GET'])
@token_required
@driver_required
def get_driver_usterki():
    user_id = g.current_user.id  # Zakładając, że `g.current_user` jest ustawiony przez dekorator `token_required`
    usterki_data = get_driver_usterki_service(user_id)
    return jsonify(usterki_data), 200

