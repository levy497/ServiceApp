################### ZESPOLY ########################
from flask import jsonify

from models.models import Zespoly, db, CzlonkowieZespolow, Uzytkownicy, Usterki, UsterkiNaZespoly


def create_zespol_service(nazwa_zespolu):
    try:
        istniejacy_zespol = Zespoly.query.filter_by(nazwa=nazwa_zespolu).first()
        if istniejacy_zespol:
            return jsonify({'message': 'Zespół o tej nazwie już istnieje.'}), 400

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

def assign_usterka_to_zespol_service(usterka_id, zespol_id):
    try:
        usterka = Usterki.query.get(usterka_id)
        if not usterka:
            return jsonify({'message': 'Usterka nie została znaleziona.'}), 404

        # Sprawdź, czy usterka jest już przypisana do innego zespołu
        istniejace_przypisanie = UsterkiNaZespoly.query.filter_by(usterki_id=usterka_id).first()
        if istniejace_przypisanie:
            return jsonify({'message': 'Usterka jest już przypisana do zespołu.'}), 400

        nowe_przypisanie = UsterkiNaZespoly(usterki_id=usterka_id, zespoly_id=zespol_id)
        db.session.add(nowe_przypisanie)
        db.session.commit()
        return jsonify({'message': 'Usterka została przypisana do zespołu.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500