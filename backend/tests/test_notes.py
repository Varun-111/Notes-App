async def create(client, title="Test note", body="text"):
    return await client.post("/notes", json={"title": title, "body": body})


async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_create_note(client):
    response = await create(client, "First note", "hello")
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "First note"
    assert data["body"] == "hello"
    assert data["id"] == 1


async def test_create_note_empty_title_rejected(client):
    response = await client.post("/notes", json={"title": ""})
    assert response.status_code == 422


async def test_create_note_missing_title_rejected(client):
    response = await client.post("/notes", json={"body": "no title"})
    assert response.status_code == 422


async def test_create_note_unknown_field_rejected(client):
    response = await client.post("/notes", json={"title": "Hi", "foo": "bar"})
    assert response.status_code == 422


async def test_list_notes(client):
    assert (await client.get("/notes")).json() == []
    await create(client, "A")
    await create(client, "B")
    titles = [n["title"] for n in (await client.get("/notes")).json()]
    assert titles == ["A", "B"]


async def test_get_note(client):
    await create(client, "A")
    response = await client.get("/notes/1")
    assert response.status_code == 200
    assert response.json()["title"] == "A"


async def test_get_missing_note_returns_404(client):
    response = await client.get("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


async def test_get_note_invalid_id_returns_422(client):
    assert (await client.get("/notes/abc")).status_code == 422


async def test_update_only_changes_sent_fields(client):
    await create(client, "Old title", "Old body")
    response = await client.patch("/notes/1", json={"body": "New body"})
    assert response.status_code == 200
    assert response.json()["title"] == "Old title"
    assert response.json()["body"] == "New body"


async def test_update_returns_fresh_updated_at(client):
    # Regression test for the MissingGreenlet bug (missing refresh after update)
    created = (await create(client)).json()
    response = await client.patch("/notes/1", json={"title": "Changed"})
    assert response.status_code == 200
    assert response.json()["updated_at"] >= created["updated_at"]


async def test_update_missing_note_returns_404(client):
    response = await client.patch("/notes/999", json={"title": "x"})
    assert response.status_code == 404


async def test_delete_note(client):
    await create(client, "A")
    assert (await client.delete("/notes/1")).status_code == 204
    assert (await client.get("/notes/1")).status_code == 404


async def test_delete_missing_note_returns_404(client):
    assert (await client.delete("/notes/999")).status_code == 404