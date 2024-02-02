from functools import wraps
from flask import g, jsonify

def service_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user.funkcje_id != 3:  # 3 to ID funkcji dla serwisantow
            return jsonify({'message': 'Tylko serwisant może wykonywać tę akcję.'}), 403
        return f(*args, **kwargs)
    return decorated_function
