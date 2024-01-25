from flask import jsonify, request
from werkzeug.security import generate_password_hash

from __init__ import db
from models.models import Uzytkownicy, Zespoly, CzlonkowieZespolow


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
################### ZESPOLY ########################
def create_zespol_service(nazwa_zespolu):
    try:
        nowy_zespol = Zespoly(nazwa=nazwa_zespolu)
        db.session.add(nowy_zespol)
        db.session.commit()
        return jsonify({'message': 'Zespół został pomyślnie utworzony.', 'zespol_id': nowy_zespol.id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
def get_zespoly_service():
    try:
        zespoly = Zespoly.query.all()
        zespoly_data = {}

        for zespol in zespoly:
            czlonkowie = CzlonkowieZespolow.query.filter_by(zespoly_id=zespol.id).all()
            czlonkowie_list = []

            for czlonek in czlonkowie:
                uzytkownik = Uzytkownicy.query.get(czlonek.uzytkownicy_id)
                if uzytkownik:
                    czlonkowie_list.append({'id': uzytkownik.id, 'imie': uzytkownik.imie, 'nazwisko': uzytkownik.nazwisko})

            zespoly_data[zespol.nazwa] = {
                'id_zespolu': zespol.id,
                'czlonkowie': czlonkowie_list
            }

        return jsonify({'zespoly': zespoly_data}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500



def assign_user_to_zespol_service(zespol_id, uzytkownik_id):
    try:
        zespol = Zespoly.query.get(zespol_id)
        uzytkownik = Uzytkownicy.query.get(uzytkownik_id)

        if not zespol:
            return jsonify({'message': 'Zespół nie został znaleziony.'}), 404
        if not uzytkownik:
            return jsonify({'message': 'Użytkownik nie został znaleziony.'}), 404

        # Sprawdź, czy użytkownik jest już przypisany do zespołu
        is_member = CzlonkowieZespolow.query.filter_by(uzytkownicy_id=uzytkownik_id, zespoly_id=zespol_id).first()
        if is_member:
            return jsonify({'message': 'Użytkownik jest już przypisany do tego zespołu.'}), 400

        nowy_czlonek = CzlonkowieZespolow(uzytkownicy_id=uzytkownik_id, zespoly_id=zespol_id)
        db.session.add(nowy_czlonek)
        db.session.commit()
        return jsonify({'message': 'Użytkownik został przypisany do zespołu.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def remove_user_from_zespol_service(zespol_id, uzytkownik_id):
    try:
        czlonek = CzlonkowieZespolow.query.filter_by(zespoly_id=zespol_id, uzytkownicy_id=uzytkownik_id).first()
        if not czlonek:
            return jsonify({'message': 'Członek zespołu nie został znaleziony.'}), 404

        db.session.delete(czlonek)
        db.session.commit()
        return jsonify({'message': 'Członek zespołu został usunięty.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
def update_zespol_service(zespol_id, nowa_nazwa):
    try:
        zespol = Zespoly.query.get(zespol_id)
        if not zespol:
            return jsonify({'message': 'Zespół nie został znaleziony.'}), 404

        zespol.nazwa = nowa_nazwa
        db.session.commit()
        return jsonify({'message': 'Nazwa zespołu została zmieniona.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def delete_zespol_service(zespol_id):
    try:
        zespol = Zespoly.query.get(zespol_id)
        if not zespol:
            return jsonify({'message': 'Zespół nie został znaleziony.'}), 404

        # Usunięcie wszystkich powiązań członków zespołu
        CzlonkowieZespolow.query.filter_by(zespoly_id=zespol_id).delete()

        # Usunięcie zespołu
        db.session.delete(zespol)
        db.session.commit()
        return jsonify({'message': 'Zespół i wszystkie jego powiązania zostały usunięte.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
