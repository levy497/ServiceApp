from flask import Blueprint, request, jsonify, g
from services.Admin.stuff_service import assign_usterka_to_zespol_service
from services.Usterki.usterki_service import create_usterka_service, get_all_usterki_service, get_usterki_for_my_team, \
    update_usterka_service
from utils.admin_utilis import admin_required
from utils.driver_utilis import driver_required
from utils.jwt_utils import token_required
from utils.service_utilis import service_required

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


@usterki_bp.route('/api/get_all_usterki', methods=['GET'])
@token_required
@admin_required
def get_all_usterki():
    return get_all_usterki_service()

####### ZESPOLY####
@usterki_bp.route('/api/assign_usterka_to_zespol', methods=['POST'])
@token_required
@admin_required
def assign_usterka_to_zespol():
    data = request.get_json()
    usterka_id = data.get('usterka_id')
    zespol_id = data.get('zespol_id')
    return assign_usterka_to_zespol_service(usterka_id, zespol_id)


@usterki_bp.route('/api/my-usterki', methods=['GET'])
@token_required
@service_required
def get_my_usterki():
    return get_usterki_for_my_team()


@usterki_bp.route('/api/usterki/<int:usterka_id>', methods=['PUT'])
@token_required
@service_required
def update_usterka(usterka_id):
    data = request.get_json()
    komentarz_serwisanta = data.get('komentarz_serwisanta')
    nowy_status_id = data.get('nowy_status_id')

    # Wywołanie funkcji serwisu do aktualizacji usterki
    response = update_usterka_service(usterka_id, komentarz_serwisanta, nowy_status_id)
    return response