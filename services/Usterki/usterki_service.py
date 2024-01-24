from models.models import Usterki, db
from flask import jsonify, request


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

def get_all_usterki_service():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated_usterki = Usterki.query.paginate(page=page, per_page=per_page, error_out=False)

    usterki_data = [{
        'id': usterka.id,
        'auto': {
            "nr_rejestracyjny": usterka.pojazdy.rejestracja,
            "rocznik": usterka.pojazdy.rocznik,
            "model": usterka.pojazdy.modele.nazwa

        },
        'uzytkownik': {
            'imie': usterka.uzytkownicy.imie,
            'nazwisko': usterka.uzytkownicy.nazwisko
        },
        'status': usterka.status.nazwa if usterka.status else 'Brak statusu',
        'priorytet': usterka.priorytet,
        'opis': usterka.opis
    } for usterka in paginated_usterki.items]

    return jsonify({
        'usterki': usterki_data,
        'total': paginated_usterki.total,
        'pages': paginated_usterki.pages,
        'current_page': page
    }), 200
