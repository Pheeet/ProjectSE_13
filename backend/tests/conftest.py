# backend/tests/conftest.py
import pytest
from app import app as flask_app, db as sqlalchemy_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
    })
    
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def db_session(app):
    connection = sqlalchemy_db.engine.connect()
    transaction = connection.begin()
    
    # ผูก session ของแอปเข้ากับ transaction นี้
    session_factory = sqlalchemy_db.sessionmaker(bind=connection)
    db_session = sqlalchemy_db.scoping.scoped_session(session_factory)
    
    sqlalchemy_db.session = db_session

    yield db_session

    # หลังเทสเสร็จ: rollback transaction และคืน connection
    db_session.remove()
    transaction.rollback()
    connection.close()