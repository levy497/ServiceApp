from models.models import Usterki, db, UsterkiNaZespoly, Pojazdy, Modele
from flask import jsonify, request, g


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


def get_usterki_for_my_team():
    # Sprawdzenie, czy użytkownik należy do jakiegoś zespołu
    if not g.current_user.czlonkowie_zespolow:
        return jsonify({'error': 'Serwisant nie jest przypisany do żadnego zespołu'}), 400

    # Pobranie ID zespołu, do którego należy użytkownik
    team_id = g.current_user.czlonkowie_zespolow[0].zespoly_id

    # Pobranie usterek przypisanych do zespołu użytkownika wraz z informacjami o samochodzie
    usterki = Usterki.query\
                     .join(UsterkiNaZespoly)\
                     .filter(UsterkiNaZespoly.zespoly_id == team_id)\
                     .join(Pojazdy)\
                     .add_columns(Usterki.id, Usterki.opis, Usterki.komentarz_serwisanta, Usterki.status_id, Pojazdy.rejestracja, Pojazdy.rocznik, Modele.nazwa.label('model'))\
                     .join(Modele)\
                     .all()

    # Przygotowanie i zwrócenie danych o usterkach
    usterki_data = [{
        'id': usterka.id,
        'opis': usterka.opis,
        'komentarz_serwisanta': usterka.komentarz_serwisanta,
        'status_id': usterka.status_id,
        'samochod': {
            'rejestracja': usterka.rejestracja,
            'rocznik': usterka.rocznik,
            'model': usterka.model
        }
    } for usterka in usterki]

    return jsonify(usterki_data), 200


def update_usterka_service(usterka_id, komentarz_serwisanta, nowy_status_id):

    # Znajdowanie usterki
    usterka = Usterki.query.get(usterka_id)
    if not usterka:
        return jsonify({'error': 'Usterka nie znaleziona'}), 404

    # Aktualizacja usterki
    if komentarz_serwisanta is not None:
        usterka.komentarz_serwisanta = komentarz_serwisanta
    if nowy_status_id is not None:
        usterka.status_id = nowy_status_id

    db.session.commit()
    return jsonify({'message': 'Usterka została zaktualizowana'}), 200