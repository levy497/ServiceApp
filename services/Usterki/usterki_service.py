from models.models import Usterki, db
from flask import jsonify

def create_usterka_service(auto_id, uzytkownicy_id, opis, priorytet):
    try:
        nowa_usterka = Usterki(
            auto_id=auto_id,
            uzytkownicy_id=uzytkownicy_id,
            opis=opis,
            priorytet=priorytet,
            status_id=1
        )
        db.session.add(nowa_usterka)
        db.session.commit()
        return jsonify({'message': 'Usterka została pomyślnie zgłoszona.'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500