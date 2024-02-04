import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from init import create_app, db
from models.models import Uzytkownicy, Funkcje
from test_config import TestConfig

class TestAuth(TestCase):

    def create_app(self):
        app = create_app(TestConfig)  # Tworzy aplikację z konfiguracją testową
        return app

    def setUp(self):
        # Tworzenie nowej bazy danych na potrzeby testu
        db.create_all()


    def tearDown(self):
        # Czyszczenie bazy danych po każdym teście
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        # Testowanie endpointu rejestracji z nowym użytkownikiem
        response = self.client.post('/api/register', json={
            'imie': 'Tomasz',
            'nazwisko': 'Nowak',
            'email': 'tomasz@example.com',
            'password': 'testowy123',
            'telefon': '987654321'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.json['message'])

        # Sprawdzenie, czy nowy użytkownik został dodany do bazy danych
        user = Uzytkownicy.query.filter_by(email='tomasz@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.imie, 'Tomasz')

    def test_login_user(self):
        # Najpierw dodaj użytkownika do bazy, aby zapewnić, że logowanie będzie możliwe
        hashed_password = generate_password_hash('test123')
        user = Uzytkownicy(
            imie='Jan',
            nazwisko='Kowalski',
            email='jan@example.com',
            telefon='123456789',
            haslo=hashed_password,
            funkcje_id=4
        )
        db.session.add(user)
        db.session.commit()

        # Logowanie istniejącego użytkownika
        response = self.client.post('/api/login', json={
            'email': 'jan@example.com',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        self.assertTrue(response.json['token'])

    def test_register_user_with_missing_fields(self):
        response = self.client.post('/api/register', json={
            'imie': 'Tomasz',
            'email': 'tomasz_missing@example.com',
            # Brak hasła i telefonu
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json)

    def test_register_user_that_already_exists(self):
        # Najpierw dodaj użytkownika
        response = self.client.post('/api/register', json={
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'email': 'existing@example.com',
            'password': 'test123',
            'telefon': '123456789'
        })
        # Następnie spróbuj zarejestrować tego samego użytkownika
        response = self.client.post('/api/register', json={
            'imie': 'Jan',
            'nazwisko': 'Kowalski',
            'email': 'existing@example.com',
            'password': 'test123',
            'telefon': '123456789'
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn('User already exists', response.json['message'])

    def test_login_with_wrong_password(self):
        # Użyj danych użytkownika z poprzedniego testu
        response = self.client.post('/api/login', json={
            'email': 'jan@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.json['message'])

    def test_login_with_missing_fields(self):
        response = self.client.post('/api/login', json={
            # Brak e-maila
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Login and password are required', response.json['message'])

        response = self.client.post('/api/login', json={
            'email': 'jan@example.com',
            # Brak hasła
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Login and password are required', response.json['message'])

if __name__ == '__main__':
    pytest.main()
