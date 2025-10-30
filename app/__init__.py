from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Imports
    from app.main.routes import main

    # Registers
    app.register_blueprint(main)

    return app