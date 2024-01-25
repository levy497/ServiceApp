from flask import jsonify, request
from werkzeug.security import generate_password_hash

from __init__ import db
from models.models import Uzytkownicy

#Wszyscy uzytkownicy
def get_all_users_service():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated_users = Uzytkownicy.query.paginate(page=page, per_page=per_page, error_out=False)

    users_data = [{
        'id': user.id,
        'imie': user.imie,
        'nazwisko': user.nazwisko,
        'email': user.email,
        'rola': user.funkcje.nazwa if user.funkcje else 'Brak roli'
    } for user in paginated_users.items]

    return jsonify({
        'users': users_data,
        'total': paginated_users.total,
        'pages': paginated_users.pages,
        'current_page': page
    }), 200
#Aktualizacja uprawnien dla danego uzytkownika
def update_user_service(user_id, user_data):
    user = Uzytkownicy.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        user.imie = user_data.get('imie', user.imie)
        user.nazwisko = user_data.get('nazwisko', user.nazwisko)
        user.email = user_data.get('email', user.email)
        user.funkcje_id = user_data.get('funkcje_id', user.funkcje_id)
        user.telefon = user_data.get('telefon', user.telefon)

        # Aktualizacja hasła, jeśli zostało podane nowe
        new_password = user_data.get('haslo')
        if new_password:
            user.haslo = generate_password_hash(new_password)

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def delete_users_service(user_id):
    try:
        user = Uzytkownicy.query.get(user_id)
        if not user:
            return jsonify({'message': 'Użytkownik nie został znaleziony.'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Użytkownik został usunięty.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
