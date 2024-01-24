from datetime import datetime, timedelta

import jwt
from flask import current_app, jsonify
from functools import wraps
from flask import request, g

from models.models import Uzytkownicy


def generate_token(user_id):
    try:
        # Ustawienie daty wygaśnięcia tokenu, np. na 1 godzinę od teraz
        exp = datetime.utcnow() + timedelta(hours=1)
        # Dodanie user_id i exp do payloadu
        token_payload = {
            'user_id': user_id,
            'exp': exp
        }
        token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    except Exception as e:
        return str(e)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Sprawdzenie, czy token jest w nagłówkach
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Dekodowanie tokenu JWT
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Uzytkownicy.query.get(data['user_id'])
            g.current_user = current_user
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
