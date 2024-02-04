import json
import pytest
from flask_testing import TestCase
from init import create_app, db
from models.models import Uzytkownicy, Usterki, Zespoly, CzlonkowieZespolow  # Zakładamy, że te modele istnieją
from test_config import TestConfig
from werkzeug.security import generate_password_hash

class TestServiceFunctions(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        super().setUp()
        db.create_all()
        self.insert_service_user_and_team()
        self.add_dummy_usterka()



    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_dummy_usterka(self):
        # Zakładamy, że funkcje do dodawania zespołu i użytkownika już istnieją
        auto_id = 1  # Przykład, musisz dodać pojazd do bazy danych
        usterka = Usterki(auto_id=auto_id, uzytkownicy_id=1, opis="Testowa usterka", priorytet=False, status_id=1)
        db.session.add(usterka)
        db.session.commit()


        # Utwórz usterkę i przypisz ją do zalogowanego serwisanta
        service_user = Uzytkownicy.query.filter_by(email="service@example.com").first()
        if service_user:
            usterka = Usterki(auto_id=auto_id, uzytkownicy_id=service_user.id, opis="Testowa usterka", priorytet=False,
                              status_id=1)
            db.session.add(usterka)
            db.session.commit()
    def insert_service_user_and_team(self):
        service_password = generate_password_hash("service_secret")
        service_user = Uzytkownicy(imie="Service", nazwisko="Technician", email="service@example.com", haslo=service_password, funkcje_id=3)
        db.session.add(service_user)
        db.session.flush()

        # Tworzenie zespołu serwisowego i przypisanie serwisanta do zespołu
        team = Zespoly(nazwa="Zespół Serwisowy")
        db.session.add(team)
        db.session.flush()

        member = CzlonkowieZespolow(uzytkownicy_id=service_user.id, zespoly_id=team.id)
        db.session.add(member)
        db.session.commit()

        self.login_as_service_user()

    def login_as_service_user(self):
        response = self.client.post('/api/login', json={
            'email': 'service@example.com',
            'password': 'service_secret'
        })
        data = json.loads(response.data.decode())
        self.service_token = data['token']

    def test_get_my_usterki(self):
        # Wysłanie żądania o pobranie usterek
        response = self.client.get(
            '/api/my-usterki',
            headers={'Authorization': f'Bearer {self.service_token}'}
        )
        # Sprawdzenie kodu statusu
        self.assertEqual(response.status_code, 200)
        # Weryfikacja treści odpowiedzi
        response_data = json.loads(response.data.decode())
        # Sprawdzenie, czy klucz 'usterki' istnieje w odpowiedzi
        self.assertIn('usterki', response_data)

        for usterka in response_data['usterki']:
            self.assertIn('id', usterka)
            self.assertIn('opis', usterka)
            self.assertIn('komentarz_serwisanta', usterka)
            self.assertIn('status_id', usterka)
            self.assertIn('samochod', usterka)
            samochod = usterka['samochod']
            self.assertIn('rejestracja', samochod)
            self.assertIn('rocznik', samochod)
            self.assertIn('model', samochod)

    def test_update_usterka(self):
        update_data = {
            'komentarz_serwisanta': 'Naprawa zakończona sukcesem',
            'nowy_status_id': 4
        }
        # Wysłanie żądania aktualizacji usterki
        response = self.client.put(
            '/api/usterki/1',
            headers={'Authorization': f'Bearer {self.service_token}'},
            json=update_data
        )
        # Sprawdzenie kodu statusu
        self.assertEqual(response.status_code, 200)
        # Weryfikacja treści odpowiedzi
        response_data = json.loads(response.data.decode())
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Usterka została zaktualizowana')


if __name__ == '__main__':
    pytest.main()
