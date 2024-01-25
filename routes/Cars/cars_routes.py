from flask import Blueprint, request
from services.TechnicalSpecialist.cars_service import add_cars, get_all_cars, delete_cars, update_cars_service
from utils.jwt_utils import token_required
from utils.technical_specialist_utilis import technical_specialist_required

cars_bp = Blueprint('cars_bp', __name__)

@cars_bp.route('/api/add_pojazd', methods=['POST'])
@token_required
@technical_specialist_required
def add_pojazd():
    data = request.get_json()
    rejestracja = data.get('rejestracja')
    nazwa_modelu = data.get('nazwa_modelu')
    parametry_techniczne = data.get('parametry_techniczne')  # Nowe pole dla parametrów technicznych modelu
    rocznik = data.get('rocznik')
    uwagi = data.get('uwagi')

    return add_cars(rejestracja, nazwa_modelu, parametry_techniczne, rocznik, uwagi)

@cars_bp.route('/api/get_all_pojazdy', methods=['GET'])
@token_required
@technical_specialist_required
def get_all_pojazdy():
    return get_all_cars()
@cars_bp.route('/api/update_car/<int:car_id>', methods=['PUT'])
@token_required
@technical_specialist_required
def update_car(car_id):
    car_data = request.json
    return update_cars_service(car_id, car_data)

@cars_bp.route('/api/delete_pojazd/<int:pojazd_id>', methods=['DELETE'])
@token_required
@technical_specialist_required
def delete_car(pojazd_id):
    return delete_cars(pojazd_id)

