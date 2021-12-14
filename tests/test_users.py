from jose import jwt
from fastapi import Response
from app.schemas import CreatedUser, Token
from app.config import settings


def test_create_user(client):
    res: Response = client.post(
        '/users/', json={'email': 'someemail@email.com', 'password': 'password12345'})
    new_user = CreatedUser(**res.json())
    assert new_user.email == 'someemail@email.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res: Response = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']})

    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=settings.algorithm)
    id: str = payload.get('user_id')

    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


def test_incorrect_login(test_user, client):
    res: Response = client.post(
        '/login', data={'username': test_user['email'], 'password': 'rendeniwrong'})
    
    assert res.status_code == 403
    assert res.json().get('detail') == 'Invalid Credentials'