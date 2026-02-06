from flask import Flask
from app.core.config import config_by_name
from app.core.extensions import db, jwt

def create_app(config_name="dev"):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config_by_name[config_name])

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)


    # Register blueprints
    register_blueprints(app)

    return app


def register_blueprints(app):
    from app.api.health import health_bp
    app.register_blueprint(health_bp)
