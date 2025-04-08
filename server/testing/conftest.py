import pytest
from app import app as flask_app
from models import db as _db
from flask_migrate import Migrate
from seed import seed_data

@pytest.fixture
def app():
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with flask_app.app_context():
        _db.create_all()
        migrate = Migrate(flask_app, _db)
        migrate.init_app(flask_app, _db)
        seed_data()  # Seed the test database with initial data
        yield flask_app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
