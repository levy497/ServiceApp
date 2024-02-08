from functools import wraps
from flask import g, jsonify

def admin_driver_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Sprawdzenie, czy zalogowany użytkownik jest administratorem lub kierowcą
        if not (g.current_user.funkcje_id == 1 or g.current_user.funkcje_id == 2):  # Sprawdzenie roli
            return jsonify({'message': 'Admin or driver access required'}), 403
        return f(*args, **kwargs)
    return decorated_function