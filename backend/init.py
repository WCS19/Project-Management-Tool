import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Set configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress deprecation warning

    # Enable CORS for all routes and origins
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Import models to register them with SQLAlchemy
        import backend.models
        # Register blueprints or routes
        from backend.routes import register_routes
        register_routes(app)
        db.create_all()

    return app