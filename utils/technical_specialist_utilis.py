from functools import wraps
from flask import g, jsonify

def technical_specialist_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user.funkcje_id != 4:  # 2 to ID funkcji dla specjalistów ds. technicznych
            return jsonify({'message': 'Tylko specjalista ds. technicznych może wykonywać tę akcję.'}), 403
        return f(*args, **kwargs)
    return decorated_function
