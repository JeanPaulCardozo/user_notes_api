def test_create_note_success(client, auth_headers):
    headers = auth_headers()

    response = client.post(
        "/notes/",
        json={"title": "First note", "content": "Some content"},
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "First note"
    assert body["content"] == "Some content"
    assert "id" in body


def test_create_note_without_auth_fails(client):
    response = client.post(
        "/notes/", json={"title": "First note", "content": "Some content"}
    )

    assert response.status_code == 401


def test_create_note_empty_title_fails(client, auth_headers):
    headers = auth_headers()

    response = client.post(
        "/notes/", json={"title": "", "content": "Some content"}, headers=headers
    )

    assert response.status_code == 422


def test_get_notes_empty_for_new_user(client, auth_headers):
    headers = auth_headers()

    response = client.get("/notes/", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


def test_get_notes_returns_only_own_notes(client, auth_headers):
    owner_headers = auth_headers(email="owner@example.com")
    other_headers = auth_headers(email="other@example.com")

    client.post(
        "/notes/",
        json={"title": "Owner note", "content": "content"},
        headers=owner_headers,
    )

    response = client.get("/notes/", headers=other_headers)

    assert response.status_code == 200
    assert response.json() == []

    response = client.get("/notes/", headers=owner_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_note_by_id(client, auth_headers):
    headers = auth_headers()
    created = client.post(
        "/notes/", json={"title": "Note", "content": "content"}, headers=headers
    ).json()

    response = client.get(f"/notes/{created['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_note_not_found(client, auth_headers):
    headers = auth_headers()

    response = client.get("/notes/9999", headers=headers)

    assert response.status_code == 404


def test_get_note_forbidden_for_other_user(client, auth_headers):
    owner_headers = auth_headers(email="owner2@example.com")
    other_headers = auth_headers(email="other2@example.com")

    created = client.post(
        "/notes/", json={"title": "Note", "content": "content"}, headers=owner_headers
    ).json()

    response = client.get(f"/notes/{created['id']}", headers=other_headers)

    assert response.status_code == 403


def test_update_note_success(client, auth_headers):
    headers = auth_headers()
    created = client.post(
        "/notes/", json={"title": "Note", "content": "content"}, headers=headers
    ).json()

    response = client.patch(
        f"/notes/{created['id']}",
        json={"title": "Updated", "content": "Updated content"},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated"
    assert body["content"] == "Updated content"


def test_update_note_not_found(client, auth_headers):
    headers = auth_headers()

    response = client.patch(
        "/notes/9999",
        json={"title": "Updated", "content": "Updated content"},
        headers=headers,
    )

    assert response.status_code == 404


def test_update_note_forbidden_for_other_user(client, auth_headers):
    owner_headers = auth_headers(email="owner3@example.com")
    other_headers = auth_headers(email="other3@example.com")

    created = client.post(
        "/notes/", json={"title": "Note", "content": "content"}, headers=owner_headers
    ).json()

    response = client.patch(
        f"/notes/{created['id']}",
        json={"title": "Hacked", "content": "Hacked content"},
        headers=other_headers,
    )

    assert response.status_code == 403


def test_delete_note_success(client, auth_headers):
    headers = auth_headers()
    created = client.post(
        "/notes/", json={"title": "Note", "content": "content"}, headers=headers
    ).json()

    response = client.delete(f"/notes/{created['id']}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/notes/{created['id']}", headers=headers)
    assert response.status_code == 404


def test_delete_note_not_found(client, auth_headers):
    headers = auth_headers()

    response = client.delete("/notes/9999", headers=headers)

    assert response.status_code == 404


def test_delete_note_forbidden_for_other_user(client, auth_headers):
    owner_headers = auth_headers(email="owner4@example.com")
    other_headers = auth_headers(email="other4@example.com")

    created = client.post(
        "/notes/", json={"title": "Note", "content": "content"}, headers=owner_headers
    ).json()

    response = client.delete(f"/notes/{created['id']}", headers=other_headers)

    assert response.status_code == 403
