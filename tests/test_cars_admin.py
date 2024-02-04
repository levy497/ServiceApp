import json
import pytest
from flask_testing import TestCase
from init import create_app, db
from models.models import Uzytkownicy  # Załóżmy, że taka klasa istnieje
from test_config import TestConfig
from werkzeug.security import generate_password_hash

class TestCarAdminRoutes(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()
        self.insert_admin_user()
        self.admin_token = self.login_as_admin()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def insert_admin_user(self):
        admin_password = generate_password_hash("admin_secret")
        admin_user = Uzytkownicy(id=1, imie="Admin", nazwisko="Admin", email="admin@example.com", haslo=admin_password, funkcje_id=1)
        db.session.add(admin_user)
        db.session.commit()

    def login_as_admin(self):
        response = self.client.post('/api/login', json={
            'email': 'admin@example.com',
            'password': 'admin_secret'
        })
        data = json.loads(response.data.decode())
        return data['token']
    def test_add_pojazd(self):
        car_data = {
            'rejestracja': 'XYZ 1234',
            'nazwa_modelu': 'Tesla Model S',
            'parametry_techniczne': 'Elektryczny, 500KM',
            'rocznik': '2020',
            'uwagi': 'Brak'
        }
        response = self.client.post(
            '/api/add_pojazd',
            headers={'Authorization': f'Bearer {self.admin_token}'},
            json=car_data
        )
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data.decode())
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Pojazd został pomyślnie dodany.')

    def test_get_all_pojazdy(self):
        self.test_add_pojazd()
        response = self.client.get(
            '/api/get_all_pojazdy',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue('pojazdy' in data)
        self.assertTrue(isinstance(data['pojazdy'], list))
        self.assertGreaterEqual(len(data['pojazdy']), 1)  # Sprawdzamy, czy jest co najmniej jeden pojazd

    def test_update_car(self):
        self.test_add_pojazd()

        # Teraz możemy zaktualizować pojazd o ID 1, zakładając, że jest to pojazd testowy dodany w setUp
        updated_car_data = {
            'rejestracja': 'XYZ 9876',
            'nazwa_modelu': 'Tesla Model X',
            'parametry_techniczne': 'Elektryczny, 700KM',
            'rocznik': '2021',
            'uwagi': 'Zaktualizowane'
        }
        response = self.client.put(
            '/api/update_car/1',  # Zakładamy, że pojazd o ID 1 istnieje
            headers={'Authorization': f'Bearer {self.admin_token}'},
            json=updated_car_data
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_car(self):
        # Dodaj pojazd, który zostanie usunięty
        self.test_add_pojazd()
        car_id = 1  # Zakładając, że test_add_pojazd() dodał pojazd o ID 1
        response = self.client.delete(
            f'/api/delete_pojazd/{car_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent_car(self):
        non_existent_car_id = 99999  # Zakładamy, że taki ID nie istnieje w bazie
        response = self.client.delete(
            f'/api/delete_pojazd/{non_existent_car_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data.decode())
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Pojazd nie został znaleziony.')


if __name__ == '__main__':
    pytest.main()
