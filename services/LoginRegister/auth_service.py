from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import Uzytkownicy
from utils.jwt_utils import generate_token
from init import db


def login_user(user_data):
    # Pobieranie danych użytkownika
    email = user_data.get('email')
    password = user_data.get('password')

    if not email or not password:
        return jsonify({'message': 'Login and password are required'}), 400

    # Wyszukiwanie użytkownika w bazie danych
    user = Uzytkownicy.query.filter(Uzytkownicy.email == email).first()

    if user and check_password_hash(user.haslo, password):
        # Generowanie tokenu JWT
        token = generate_token(user.id)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
def register_user(user_data):
    # Pobieranie danych rejestracyjnych
    imie = user_data.get('imie')
    nazwisko = user_data.get('nazwisko')
    email = user_data.get('email')
    password = user_data.get('password')
    telefon = user_data.get('telefon')

    if not all([imie, nazwisko, email, password]):
        return jsonify({'message': 'All fields are required'}), 400

    # Sprawdzenie, czy użytkownik już istnieje
    existing_user = Uzytkownicy.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    # Tworzenie nowego użytkownika
    new_user = Uzytkownicy(
        imie=imie,
        nazwisko=nazwisko,
        email=email,
        telefon=telefon,
        haslo=generate_password_hash(password),
        funkcje_id=4  # ID dla domyślnej roli 'Użytkownik'
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
