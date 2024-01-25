from models.models import Pojazdy, Modele, db
from flask import jsonify, request


def get_all_cars():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated_pojazdy = Pojazdy.query.paginate(page=page, per_page=per_page, error_out=False)

    pojazdy_data = [{
        'id': pojazd.id,
        'rejestracja': pojazd.rejestracja,
        'model': pojazd.modele.nazwa if pojazd.modele else 'Brak modelu',
        'rocznik': pojazd.rocznik,
        'uwagi': pojazd.uwagi if pojazd.uwagi else "Brak uwag",
        "parametry techniczne": pojazd.modele.parametry_techniczne if pojazd.modele else "Brak parametrów technicznych"
    } for pojazd in paginated_pojazdy.items]

    return jsonify({
        'pojazdy': pojazdy_data,
        'total': paginated_pojazdy.total,
        'pages': paginated_pojazdy.pages,
        'current_page': page
    }), 200
def add_cars(rejestracja, nazwa_modelu, parametry_techniczne, rocznik, uwagi):
    try:
        # Sprawdź, czy model już istnieje
        model = Modele.query.filter_by(nazwa=nazwa_modelu).first()

        # Jeśli model nie istnieje, utwórz nowy
        if not model:
            model = Modele(nazwa=nazwa_modelu, parametry_techniczne=parametry_techniczne)
            db.session.add(model)
            db.session.flush()  # Flush, aby uzyskać ID dla nowo utworzonego modelu

        nowy_pojazd = Pojazdy(
            rejestracja=rejestracja,
            modele_id=model.id,
            rocznik=rocznik,
            uwagi=uwagi
        )
        db.session.add(nowy_pojazd)
        db.session.commit()
        return jsonify({'message': 'Pojazd został pomyślnie dodany.'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


def update_cars_service(car_id, car_data):
    car = Pojazdy.query.get(car_id)
    if not car:
        return jsonify({'message': 'Car not found'}), 404

    try:
        car.rejestracja = car_data.get('rejestracja', car.rejestracja)
        car.rocznik = car_data.get('rocznik', car.rocznik)
        car.uwagi = car_data.get('uwagi', car.uwagi)

        # Zaktualizuj model, jeśli dane zostały dostarczone
        if 'nazwa_modelu' in car_data or 'parametry_techniczne' in car_data:
            model_nazwa = car_data.get('nazwa_modelu')
            model = Modele.query.filter_by(nazwa=model_nazwa).first()

            # Jeśli model nie istnieje, utwórz nowy
            if not model:
                model = Modele(nazwa=model_nazwa, parametry_techniczne=car_data.get('parametry_techniczne'))
                db.session.add(model)
                db.session.flush()  # Flush, aby uzyskać ID dla nowo utworzonego modelu

            # Aktualizuj istniejący model
            else:
                model.parametry_techniczne = car_data.get('parametry_techniczne', model.parametry_techniczne)

            # Przypisz model do pojazdu
            car.modele_id = model.id

        db.session.commit()
        return jsonify({'message': 'Car (and model if new) updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


def delete_cars(pojazd_id):
    try:
        pojazd = Pojazdy.query.get(pojazd_id)
        if not pojazd:
            return jsonify({'message': 'Pojazd nie został znaleziony.'}), 404

        db.session.delete(pojazd)
        db.session.commit()
        return jsonify({'message': 'Pojazd został usunięty.'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500