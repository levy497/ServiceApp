from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()  # Inicjalizacja db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Powiązanie db z aplikacją

    with app.app_context():
        from routes.LoginRegister import auth
        from routes.Admin import admin_routes
        from routes.Usterki import usterki_routes
        from routes.Cars import cars_routes
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(usterki_routes.usterki_bp)
        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(cars_routes.cars_bp)

        #db.create_all()

    return app
