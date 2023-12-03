from flask import Blueprint, request
from services.auth_service import login_user, register_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Logowanie użytkownika
    return login_user(request.json)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Rejestracja użytkownika
    return register_user(request.json)
