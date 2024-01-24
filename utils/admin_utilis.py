from functools import wraps
from flask import g, jsonify

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_admin = 1  # ID administratora
        # Sprawdzenie, czy zalogowany użytkownik jest administratorem
        if g.current_user.funkcje_id != id_admin:  # id_admin to ID roli admina w bazie danych
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function