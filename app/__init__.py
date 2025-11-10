from flask import Flask
from flask_login import LoginManager

from .models.models import database, User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'supersecretkey'
    
    # Init
    database.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Crear tablas
    with app.app_context():
        database.create_all()

    # Configuracion de login_manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Imports
    from app.main.routes import main
    from app.book.routes import book
    from app.auth.routes import auth
    from app.shop.routes import shop
    from app.admin.routes import admin

    # Registers
    app.register_blueprint(main)
    app.register_blueprint(book)
    app.register_blueprint(auth)
    app.register_blueprint(shop)
    app.register_blueprint(admin)

    return app