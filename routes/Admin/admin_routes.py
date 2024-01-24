from flask import Blueprint, request
from services.Admin.admin_service import get_all_users_service, update_user_service, delete_users_service
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
