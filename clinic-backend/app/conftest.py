import pytest
from app import create_app
from app.core.extensions import db


@pytest.fixture(scope="session")
def app():
    """Create a Flask app instance for the tests."""
    app = create_app("test")
    yield app

@pytest.fixture(scope="function")
def db_session(app):
    """Provide a clean database for each test."""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
