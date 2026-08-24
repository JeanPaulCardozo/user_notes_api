def test_register_user_success(client):
    response = client.post(
        "/users/register",
        json={"email": "new@example.com", "password": "supersecret"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert "id" in body
    assert "password" not in body


def test_register_duplicate_email_fails(client, register_user):
    register_user(email="dup@example.com")

    response = client.post(
        "/users/register",
        json={"email": "dup@example.com", "password": "password123"},
    )

    assert response.status_code == 400


def test_register_invalid_email_fails(client):
    response = client.post(
        "/users/register",
        json={"email": "not-an-email", "password": "password123"},
    )

    assert response.status_code == 422


def test_register_password_too_short_fails(client):
    response = client.post(
        "/users/register",
        json={"email": "short@example.com", "password": "short"},
    )

    assert response.status_code == 422


def test_login_success(client, register_user):
    register_user(email="login@example.com", password="password123")

    response = client.post(
        "/users/login",
        data={"username": "login@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_fails(client, register_user):
    register_user(email="login2@example.com", password="password123")

    response = client.post(
        "/users/login",
        data={"username": "login2@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401


def test_login_nonexistent_user_fails(client):
    response = client.post(
        "/users/login",
        data={"username": "ghost@example.com", "password": "password123"},
    )

    assert response.status_code == 401


def test_read_current_user(client, auth_headers):
    headers = auth_headers(email="me@example.com")

    response = client.get("/users/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_read_current_user_without_token_fails(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_read_current_user_invalid_token_fails(client):
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer invalid.token.value"}
    )

    assert response.status_code == 401
