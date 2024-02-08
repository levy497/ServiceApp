
from models.models import Usterki, UsterkiNaZespoly, Zespoly


# services/drivers_service.py
from flask import request
from models.models import db, Usterki, UsterkiNaZespoly, Zespoly


def get_driver_usterki_service(user_id):
    strona = request.args.get('page', 1, type=int)
    na_strone = request.args.get('per_page', 10, type=int)

    paginowane_usterki = (db.session.query(Usterki)
                          .outerjoin(UsterkiNaZespoly, Usterki.id == UsterkiNaZespoly.usterki_id)
                          .outerjoin(Zespoly, Zespoly.id == UsterkiNaZespoly.zespoly_id)
                          .filter(Usterki.uzytkownicy_id == user_id)
                          .paginate(page=strona, per_page=na_strone, error_out=False))

    usterki_data = []
    for usterka in paginowane_usterki.items:
        zespol_data = []
        # Dla każdej usterki zbieramy informacje o przypisanych zespołach
        for relacja in usterka.usterki_na_zespoly:
            zespol = relacja.zespoly  # Dostęp do obiektu Zespoly przez relację UsterkiNaZespoly
            zespol_data.append({'nazwa': zespol.nazwa})

        # Jeśli lista zespol_data jest pusta, oznacza to, że usterka nie jest przypisana do żadnego zespołu
        if not zespol_data:
            zespol_data = 'Usterka nie jest jeszcze przypisana do zespołu'

        usterki_data.append({
            'id': usterka.id,
            'opis': usterka.opis,
            'priorytet': usterka.priorytet,
            'status': usterka.status.nazwa if usterka.status else 'Brak statusu',
            'zespół': zespol_data,
            'komentarz_serwisanta': usterka.komentarz_serwisanta
        })

    return {
        'usterki': usterki_data,
        'total': paginowane_usterki.total,
        'pages': paginowane_usterki.pages,
        'current_page': strona
    }


