from flask import Flask, jsonify
from app.core.config import config_by_name
from app.core.extensions import db, jwt
from app.core.logger import setup_logger
from dotenv import load_dotenv
import os

#todo: remove this when using alembic.
#uncomment while running alembic migrations.
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager

# db = SQLAlchemy()
# jwt = JWTManager()

load_dotenv() 
def create_app(config_name="dev"):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config_by_name[config_name])

    # Setup Logging
    setup_logger(app)

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)


    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_blueprints(app):
    from app.auth.api import auth_bp
    from app.admin.api import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)


def register_error_handlers(app):
    from marshmallow import ValidationError as MarshmallowValidationError
    from app.core.exceptions import (
        AuthenticationError,
        AuthorizationError,
        ResourceNotFoundError,
        ConflictError,
        ValidationError,
    )

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        return jsonify(
            {"error": "authentication_error", "message": str(error)}
        ), 401

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error):
        return jsonify(
            {"error": "authorization_error", "message": str(error)}
        ), 403

    @app.errorhandler(ResourceNotFoundError)
    def handle_not_found_error(error):
        return jsonify(
            {"error": "not_found", "message": str(error)}
        ), 404

    @app.errorhandler(ConflictError)
    def handle_conflict_error(error):
        return jsonify(
            {"error": "conflict", "message": str(error)}
        ), 409

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify(
            {"error": "validation_error", "message": str(error)}
        ), 422

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_validation_error(error):
        # Reuse the same payload shape, but include field-level messages.
        return jsonify(
            {
                "error": "validation_error",
                "message": "Invalid request data",
                "details": error.messages,
            }
        ), 422
