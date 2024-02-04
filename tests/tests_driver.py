import json
import pytest
from flask_testing import TestCase
from init import create_app, db
from models.models import Uzytkownicy, Usterki  # Zakładamy, że te modele istnieją
from test_config import TestConfig
from werkzeug.security import generate_password_hash

class TestDriverFunctions(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()
        self.insert_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def insert_user(self):
        driver_password = generate_password_hash("driver_secret")
        driver_user = Uzytkownicy(imie="Driver", nazwisko="Testowy", email="driver@example.com", haslo=driver_password, funkcje_id=2)
        db.session.add(driver_user)
        db.session.commit()
        self.login_as_driver()

    def login_as_driver(self):
        response = self.client.post('/api/login', json={
            'email': 'driver@example.com',
            'password': 'driver_secret'
        })
        data = json.loads(response.data.decode())
        self.driver_token = data['token']

    def test_create_issue_success(self):
        # Przygotowanie danych usterki
        issue_data = {
            'auto_id': 1,
            'opis': 'Problem z silnikiem',
            'priorytet': True
        }
        # Wysłanie żądania
        response = self.client.post(
            '/api/add_issue',
            headers={'Authorization': f'Bearer {self.driver_token}'},
            json=issue_data
        )
        # Sprawdzenie kodu statusu
        self.assertEqual(response.status_code, 201)
        # Weryfikacja treści odpowiedzi
        response_data = json.loads(response.data.decode())
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Usterka została pomyślnie zgłoszona.')
        # Sprawdzenie, czy usterka została faktycznie dodana do bazy
        issues = Usterki.query.all()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].opis, 'Problem z silnikiem')

    def test_create_issue_failure_invalid_auto_id(self):
        # Przygotowanie niepoprawnych danych usterki (niepoprawne auto_id)
        issue_data = {
            'auto_id': 'niepoprawne_id',
            'opis': 'Problem z silnikiem',
            'priorytet': True
        }
        # Wysłanie żądania
        response = self.client.post(
            '/api/add_issue',
            headers={'Authorization': f'Bearer {self.driver_token}'},
            json=issue_data
        )
        # Sprawdzenie kodu statusu
        self.assertEqual(response.status_code, 400)
        # Weryfikacja treści odpowiedzi
        response_data = json.loads(response.data.decode())
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'auto_id must be an integer')

    def test_get_driver_usterki_empty_list(self):
        # Wysłanie żądania o pobranie usterek, gdy lista jest pusta
        response = self.client.get(
            '/api/driver/usterki',
            headers={'Authorization': f'Bearer {self.driver_token}'}
        )
        # Sprawdzenie kodu statusu
        self.assertEqual(response.status_code, 200)
        # Weryfikacja treści odpowiedzi
        response_data = json.loads(response.data.decode())
        self.assertIn('usterki', response_data)
        self.assertEqual(len(response_data['usterki']), 0)

    def test_get_driver_usterki_non_empty_list(self):
        # Najpierw dodajmy usterkę, aby lista nie była pusta
        self.test_create_issue_success()
        # Wysłanie żądania o pobranie usterek
        response = self.client.get(
            '/api/driver/usterki',
            headers={'Authorization': f'Bearer {self.driver_token}'}
        )
        # Sprawdzenie kodu statusu
        self.assertEqual(response.status_code, 200)
        # Weryfikacja treści odpowiedzi
        response_data = json.loads(response.data.decode())
        self.assertIn('usterki', response_data)
        self.assertGreater(len(response_data['usterki']), 0)
        # Sprawdzenie szczegółów pierwszej usterki
        first_issue = response_data['usterki'][0]
        self.assertIn('opis', first_issue)
        self.assertEqual(first_issue['opis'], 'Problem z silnikiem')
        self.assertIn('priorytet', first_issue)
        self.assertTrue(first_issue['priorytet'])
