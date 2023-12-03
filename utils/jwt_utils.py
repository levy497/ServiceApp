import jwt
from flask import current_app

def generate_token(user_id):
    # Generowanie tokena JWT
    try:
        token = jwt.encode({'user_id': user_id}, current_app.config['SECRET_KEY'])
        return token
    except Exception as e:
        return str(e)
