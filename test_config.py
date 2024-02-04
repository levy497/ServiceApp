import os
from dotenv import load_dotenv

from config import Config

load_dotenv()

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Użycie bazy danych SQLite w pamięci
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Wyłączenie ochrony CSRF dla testów

    # Ustawienie tylko zmiennej środowiskowej SECRET_KEY z .env
    SECRET_KEY = os.environ.get('SECRET_KEY')
