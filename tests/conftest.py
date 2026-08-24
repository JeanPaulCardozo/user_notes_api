import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from user_notes.database import Base, get_db
from user_notes.main import app

# Register both models on Base.metadata before create_all is called.
from user_notes.models import notes as notes_model  # noqa: F401
from user_notes.models import users as users_model  # noqa: F401


@pytest.fixture()
def engine():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture()
def client(engine):
    testing_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


DEFAULT_EMAIL = "user@example.com"
DEFAULT_PASSWORD = "password123"


@pytest.fixture()
def register_user(client):
    def _register(email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
        return client.post(
            "/users/register", json={"email": email, "password": password}
        )

    return _register


@pytest.fixture()
def auth_headers(client, register_user):
    def _auth_headers(email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD):
        register_user(email, password)
        response = client.post(
            "/users/login",
            data={"username": email, "password": password},
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers
