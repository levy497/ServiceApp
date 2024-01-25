from flask import Blueprint, request
from services.Admin.admin_service import get_all_users_service, update_user_service, delete_users_service, \
    create_zespol_service, get_zespoly_service, assign_user_to_zespol_service, remove_user_from_zespol_service, \
    update_zespol_service, delete_zespol_service
from utils.admin_utilis import admin_required
from utils.jwt_utils import token_required

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/api/users', methods=['GET'])
@token_required
@admin_required
def get_all_users():
    return get_all_users_service()

@admin_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(user_id):
    user_data = request.json
    return update_user_service(user_id, user_data)
@admin_bp.route('/api/delete_users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_id):
    return delete_users_service(user_id)
################### ZESPOLY ########################
@admin_bp.route('/api/create_zespol', methods=['POST'])
@token_required
@admin_required
def create_zespol():
    data = request.get_json()
    nazwa_zespolu = data.get('nazwa')
    return create_zespol_service(nazwa_zespolu)
@admin_bp.route('/api/get_zespoly', methods=['GET'])
@token_required
@admin_required
def get_zespoly():
    return get_zespoly_service()
@admin_bp.route('/api/assign_user_to_zespol', methods=['POST'])
@token_required
@admin_required
def assign_user_to_zespol():
    data = request.get_json()
    zespol_id = data.get('zespol_id')
    uzytkownik_id = data.get('uzytkownik_id')
    return assign_user_to_zespol_service(zespol_id, uzytkownik_id)
@admin_bp.route('/api/remove_user_from_zespol', methods=['DELETE'])
@token_required
@admin_required
def remove_user_from_zespol():
    data = request.get_json()
    zespol_id = data.get('zespol_id')
    uzytkownik_id = data.get('uzytkownik_id')
    return remove_user_from_zespol_service(zespol_id, uzytkownik_id)
@admin_bp.route('/api/update_zespol/<int:zespol_id>', methods=['PUT'])
@token_required
@admin_required
def update_zespol(zespol_id):
    data = request.get_json()
    nowa_nazwa = data.get('nowa_nazwa')
    return update_zespol_service(zespol_id, nowa_nazwa)

@admin_bp.route('/api/delete_zespol/<int:zespol_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_zespol(zespol_id):
    return delete_zespol_service(zespol_id)



