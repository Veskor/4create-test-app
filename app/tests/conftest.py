# tests/conftest.py
import pytest
from app.core.db.session import get_db, Base
from app.core.db.mock_session import engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv

load_dotenv(".env")


@pytest.fixture(scope="session")
def create_tables():
    Base.metadata.create_all(bind=engine)  # Use the engine
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(create_tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Enable nested transactions
    session.begin_nested()

    try:
        yield session
    finally:
        transaction.rollback()  # Explicit rollback after test
        session.close()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            db = db_session
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
