from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import Response
from app.database import get_db, Base
from app.main import app
from app.config import settings
from app.schemas import CreatedUser
import pytest


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)  # drops table after running tests
    # creates tables before running tests
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


def test_root(client):
    res: Response = client.get('/')
    assert res.json().get('message') == 'nothing to see here'
    assert res.status_code == 200


def test_create_user(client):
    res: Response = client.post(
        '/users/', json={'email': 'someemail@email.com', 'password': 'password12345'})
    new_user = CreatedUser(**res.json())
    assert new_user.email == 'someemail@email.com'
    assert res.status_code == 201
