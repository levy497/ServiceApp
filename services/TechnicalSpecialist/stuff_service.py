from flask import jsonify

from models.models import Usterki, UsterkiNaZespoly, db


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
