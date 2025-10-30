from flask import Flask
from .models.models import database


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'supersecretkey'
    
    # Init
    database.init_app(app)

    # Crear tablas
    with app.app_context():
        database.create_all()

    # Imports
    from app.main.routes import main
    from app.book.routes import book

    # Registers
    app.register_blueprint(main)
    app.register_blueprint(book)

    return app