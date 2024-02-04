import json
import os

import pytest
from flask_testing import TestCase
from init import create_app, db
from models.models import Uzytkownicy, Funkcje
from test_config import TestConfig
from werkzeug.security import generate_password_hash


class TestAdminRoutes(TestCase):

    def create_app(self):
        # Ustawia aplikację Flask na konfigurację testową
        app = create_app(TestConfig)
        return app

    def setUp(self):
        # Ustawia bazę danych przed testem
        db.create_all()
        self.insert_admin_user()
        self.admin_token = self.login_as_admin()

    def tearDown(self):
        # Czyści bazę danych po każdym teście
        db.session.remove()
        db.drop_all()

    def insert_admin_user(self):
        # Dodaje użytkownika admina do testów
        admin_password = generate_password_hash("admin_secret")
        admin_user = Uzytkownicy(id=1, imie="Admin", nazwisko="Admin", email="admin@example.com", haslo=admin_password, funkcje_id=1)
        db.session.add(admin_user)
        db.session.commit()

    def login_as_admin(self):
        # Symuluje logowanie admina i zwraca token JWT
        response = self.client.post('/api/login', json={
            'email': 'admin@example.com',
            'password': 'admin_secret'
        })
        data = json.loads(response.data.decode())
        return data['token']

    def test_get_all_users_unauthorized(self):
        # Testuje dostęp do listy użytkowników bez autoryzacji
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 401)

    def test_get_all_users_authorized(self):
        # Testuje dostęp do listy użytkowników z autoryzacją
        response = self.client.get(
            '/api/users',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_get_all_users_pagination(self):
        # Testuje paginację listy użytkowników
        self.add_multiple_users(20)  # Dodaje 20 użytkowników dla testu paginacji
        response = self.client.get(
            '/api/users?page=1&per_page=10',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['users']), 10)
        self.assertEqual(data['total'], 21)  # Uwzględnia admina
        self.assertEqual(data['pages'], 3)  #  oczekujemy 3 stron

    def add_multiple_users(self, number):
        # Pomocnicza funkcja do dodawania wielu użytkowników
        for i in range(number):
            user = Uzytkownicy(
                imie=f"User{i}",
                nazwisko=f"Test{i}",
                email=f"user{i}@example.com",
                haslo=generate_password_hash(f"password{i}"),
                funkcje_id=2
            )
            db.session.add(user)
        db.session.commit()

    def test_update_user(self):
        # Testuje aktualizację danych użytkownika
        self.add_user_for_update_or_delete()  # Dodaje użytkownika przed aktualizacją
        user_data = {
            'imie': 'UpdatedName',
            'nazwisko': 'UpdatedSurname',
            'email': 'updated@example.com',
            'funkcje_id': 3,
            'telefon': '123456789',
            'haslo': 'new_secret'
        }
        user_id = 2  # Zakładamy, że użytkownik do aktualizacji ma ID 2
        response = self.client.put(
            f'/api/users/{user_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'},
            json=user_data
        )
        self.assertEqual(response.status_code, 200)
        updated_user = Uzytkownicy.query.get(user_id)
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.imie, 'UpdatedName')

    def test_delete_user(self):
        # Testuje usuwanie użytkownika
        user_to_delete = self.add_user_for_update_or_delete()
        user_id_to_delete = user_to_delete.id
        response = self.client.delete(
            f'/api/delete_users/{user_id_to_delete}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)  # Oczekiwany status po pomyślnym usunięciu
        self.assertIsNone(Uzytkownicy.query.get(user_id_to_delete))  # Upewnienie się, że użytkownik został usunięty

    def add_user_for_update_or_delete(self):
        # Pomocnicza funkcja do dodawania użytkownika przed aktualizacją/usunięciem
        user = Uzytkownicy(
            imie="ToUpdateOrDelete",
            nazwisko="User",
            email="updateordelete@example.com",
            haslo=generate_password_hash("secret"),
            funkcje_id=2
        )
        db.session.add(user)
        db.session.commit()
        return user

if __name__ == '__main__':
    pytest.main()
