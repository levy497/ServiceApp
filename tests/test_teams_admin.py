import json
import pytest
from flask_testing import TestCase
from init import create_app, db
from models.models import Uzytkownicy
from test_config import TestConfig
from werkzeug.security import generate_password_hash

class TestTeamAdminRoutes(TestCase):

    def create_app(self):
        # Ustawia aplikację Flask na konfigurację testową
        app = create_app(TestConfig)
        return app

    def setUp(self):
        # Ustawia bazę danych przed testem
        db.create_all()
        self.insert_admin_user()
        self.insert_technican_user()
        self.admin_token = self.login_as_admin()

    def tearDown(self):
        # Czyści bazę danych po każdym teście
        db.session.remove()
        db.drop_all()

    def insert_admin_user(self):
        # Dodaje użytkownika admina do testów
        admin_password = generate_password_hash("admin_secret")
        admin_user = Uzytkownicy(id=1, imie="Admin", nazwisko="Admin", email="admin@example.com", haslo=admin_password,
                                 funkcje_id=1)
        db.session.add(admin_user)
        db.session.commit()
    def insert_technican_user(self):
        technican_password = generate_password_hash('technican_secret')
        technican_user = Uzytkownicy(id=2, imie="Serwisant", nazwisko="Serwisant", email="serwisant@example.com", haslo=technican_password,
                                     funkcje_id=3)
        db.session.add(technican_user)
        db.session.commit()


    def login_as_admin(self):
        # Symuluje logowanie admina i zwraca token JWT
        response = self.client.post('/api/login', json={
            'email': 'admin@example.com',
            'password': 'admin_secret'
        })
        data = json.loads(response.data.decode())
        return data['token']

    def login_as_admin(self):
        response = self.client.post('/api/login', data=json.dumps({
            'email': 'admin@example.com',
            'password': 'admin_secret'
        }), content_type='application/json')
        return json.loads(response.data.decode())['token']

    def test_create_zespol(self):
        response = self.client.post(
            '/api/create_zespol',
            headers={'Authorization': f'Bearer {self.admin_token}'},
            data=json.dumps({'nazwa': 'Zespół Testowy'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Zespół został pomyślnie utworzony.')

    def test_get_zespoly(self):
        # Najpierw dodajmy zespół do bazy danych
        self.test_create_zespol()

        response = self.client.get(
            '/api/get_zespoly',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('zespoly', data)
        self.assertTrue(len(data['zespoly']) > 0)

    def test_assign_user_to_zespol(self):
        # Zakładamy, że zespół i użytkownik już istnieją
        self.test_create_zespol()
        zespol_id = 1  # Przykładowe ID zespołu
        uzytkownik_id = 2  # Przykładowe ID użytkownika

        response = self.client.post(
            '/api/assign_user_to_zespol',
            headers={'Authorization': f'Bearer {self.admin_token}'},
            data=json.dumps({'zespol_id': zespol_id, 'uzytkownik_id': uzytkownik_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Użytkownik został przypisany do zespołu.')

    def test_remove_user_from_zespol(self):
        # Zakładamy, że użytkownik został już przypisany do zespołu
        self.test_assign_user_to_zespol()
        zespol_id = 1
        uzytkownik_id = 2

        response = self.client.delete(
            '/api/remove_user_from_zespol',
            headers={'Authorization': f'Bearer {self.admin_token}'},
            data=json.dumps({'zespol_id': zespol_id, 'uzytkownik_id': uzytkownik_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Członek zespołu został usunięty.')

    def test_update_zespol(self):
        # Najpierw dodajmy zespół do bazy danych
        self.test_create_zespol()
        zespol_id = 1  # Przykładowe ID zespołu

        response = self.client.put(
            f'/api/update_zespol/{zespol_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'},
            data=json.dumps({'nowa_nazwa': 'Zaktualizowany Zespół Testowy'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Nazwa zespołu została zmieniona.')

    def test_delete_zespol(self):
        # Najpierw dodajmy zespół do bazy danych
        self.test_create_zespol()
        zespol_id = 1  # Przykładowe ID zespołu

        response = self.client.delete(
            f'/api/delete_zespol/{zespol_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Zespół i wszystkie jego powiązania zostały usunięte.')


if __name__ == '__main__':
    pytest.main()
