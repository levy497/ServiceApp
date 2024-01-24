from functools import wraps
from flask import g, jsonify

def driver_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user.funkcje_id != 2:  # 2 to ID funkcji dla kierowców
            return jsonify({'message': 'Tylko kierowca może wykonywać tę akcję.'}), 403
        return f(*args, **kwargs)
    return decorated_function
