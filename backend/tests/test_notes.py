def create(client, title="Test note", body="text"):
    return client.post("/notes", json={"title": title, "body": body})


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_note(client):
    response = create(client, "First note", "hello")
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "First note"
    assert data["body"] == "hello"
    assert data["id"] == 1


def test_create_note_empty_title_rejected(client):
    assert client.post("/notes", json={"title": ""}).status_code == 422


def test_create_note_missing_title_rejected(client):
    assert client.post("/notes", json={"body": "no title"}).status_code == 422


def test_create_note_unknown_field_rejected(client):
    assert client.post("/notes", json={"title": "Hi", "foo": "bar"}).status_code == 422


def test_list_notes(client):
    assert client.get("/notes").json() == []
    create(client, "A")
    create(client, "B")
    titles = [n["title"] for n in client.get("/notes").json()]
    assert titles == ["A", "B"]


def test_get_note(client):
    create(client, "A")
    response = client.get("/notes/1")
    assert response.status_code == 200
    assert response.json()["title"] == "A"


def test_get_missing_note_returns_404(client):
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


def test_get_note_invalid_id_returns_422(client):
    assert client.get("/notes/abc").status_code == 422


def test_update_only_changes_sent_fields(client):
    create(client, "Old title", "Old body")
    response = client.patch("/notes/1", json={"body": "New body"})
    assert response.status_code == 200
    assert response.json()["title"] == "Old title"
    assert response.json()["body"] == "New body"


def test_update_missing_note_returns_404(client):
    assert client.patch("/notes/999", json={"title": "x"}).status_code == 404


def test_delete_note(client):
    create(client, "A")
    assert client.delete("/notes/1").status_code == 204
    assert client.get("/notes/1").status_code == 404


def test_delete_missing_note_returns_404(client):
    assert client.delete("/notes/999").status_code == 404