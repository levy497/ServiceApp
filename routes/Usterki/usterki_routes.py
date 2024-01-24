from flask import Blueprint, request, jsonify, g

from services.Usterki.usterki_service import create_usterka_service
from utils.driver_utilis import driver_required
from utils.jwt_utils import token_required

usterki_bp = Blueprint('usterki_bp', __name__)

@usterki_bp.route('/api/add_issue', methods=['POST'])
@token_required
@driver_required
def create_issue():
    if g.current_user.funkcje_id != 2:
        return jsonify({'message': 'Tylko kierowca może zgłaszać usterki.'}), 403

    data = request.get_json()
    auto_id = data.get('auto_id')
    opis = data.get('opis')
    priorytet = data.get('priorytet', False)

    if not isinstance(auto_id, int):
        return jsonify({'message': 'auto_id must be an integer'}), 400
    return create_usterka_service(auto_id=auto_id, uzytkownicy_id=g.current_user.id, opis=opis, priorytet=priorytet)