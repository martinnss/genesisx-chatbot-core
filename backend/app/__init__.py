from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app)  
    CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})

    db.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        from . import models
        db.create_all()

    return app
