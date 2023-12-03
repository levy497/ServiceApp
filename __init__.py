from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()  # Inicjalizacja db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Powiązanie db z aplikacją

    with app.app_context():
        from routes import auth  # Import wewnątrz kontekstu aplikacji
        app.register_blueprint(auth.auth_bp)

        db.create_all()

    return app
