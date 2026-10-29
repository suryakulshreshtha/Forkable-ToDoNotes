"""Chapter 05: routes, forms, the JSON API and the two safety checks.

Flask's test client sends requests straight into the app object, so these run
in milliseconds and need no browser and no open port.
"""

from flask.testing import FlaskClient


def make_note(client: FlaskClient, **fields) -> dict:
    response = client.post("/api/notes", json=fields)
    assert response.status_code == 201
    return response.get_json()


# ------------------------------------------------------------------ pages
def test_home_shows_empty_state(client: FlaskClient) -> None:
    page = client.get("/").get_data(as_text=True)
    assert "No notes yet" in page


def test_create_via_form_redirects_to_editor(client: FlaskClient) -> None:
    response = client.post("/notes", data={"title": "Groceries", "body": "milk"})
    assert response.status_code == 302
    assert response.headers["Location"].startswith("/notes/1")
    page = client.get("/notes/1").get_data(as_text=True)
    assert 'value="Groceries"' in page


def test_update_via_form(client: FlaskClient) -> None:
    note = make_note(client, title="old")
    client.post(f"/notes/{note['id']}", data={"title": "new", "body": "", "pinned": "on"})
    data = client.get(f"/api/notes/{note['id']}").get_json()
    assert (data["title"], data["pinned"]) == ("new", True)


def test_pin_and_delete_via_form(client: FlaskClient) -> None:
    note = make_note(client, title="t")
    client.post(f"/notes/{note['id']}/pin")
    assert client.get(f"/api/notes/{note['id']}").get_json()["pinned"] is True
    client.post(f"/notes/{note['id']}/delete")
    assert client.get(f"/api/notes/{note['id']}").status_code == 404


def test_checklist_forms(client: FlaskClient) -> None:
    note = make_note(client, title="t")
    client.post(f"/notes/{note['id']}/items", data={"text": "buy milk"})
    item = client.get(f"/api/notes/{note['id']}").get_json()["items"][0]
    client.post(f"/items/{item['id']}/toggle")
    assert client.get(f"/api/notes/{note['id']}").get_json()["items"][0]["done"] is True
    client.post(f"/items/{item['id']}/delete")
    assert client.get(f"/api/notes/{note['id']}").get_json()["items"] == []


def test_unknown_note_page_is_404(client: FlaskClient) -> None:
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert "Not found" in response.get_data(as_text=True)


def test_note_text_is_escaped_not_executed(client: FlaskClient) -> None:
    make_note(client, title="<script>alert(1)</script>")
    page = client.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page


# -------------------------------------------------------------------- API
def test_api_create_with_items(client: FlaskClient) -> None:
    note = make_note(client, title="Trip", items=["passport", "charger"])
    assert [i["text"] for i in note["items"]] == ["passport", "charger"]


def test_api_rejects_non_json(client: FlaskClient) -> None:
    response = client.post("/api/notes", data="title=x")
    assert response.status_code == 400
    assert "JSON" in response.get_json()["error"]


def test_api_rejects_wrong_types(client: FlaskClient) -> None:
    note = make_note(client, title="t")
    response = client.patch(f"/api/notes/{note['id']}", json={"pinned": "yes"})
    assert response.status_code == 400


def test_api_patch_and_delete(client: FlaskClient) -> None:
    note = make_note(client, title="t")
    assert client.patch(f"/api/notes/{note['id']}", json={"body": "b"}).get_json()["body"] == "b"
    assert client.delete(f"/api/notes/{note['id']}").status_code == 204
    assert client.get(f"/api/notes/{note['id']}").get_json()["error"].startswith("Note")


def test_api_item_toggle(client: FlaskClient) -> None:
    note = make_note(client, title="t", items=["x"])
    item_id = note["items"][0]["id"]
    assert client.patch(f"/api/items/{item_id}", json={"done": True}).get_json()["done"] is True
    assert client.patch(f"/api/items/{item_id}", json={}).status_code == 400
    assert client.delete(f"/api/items/{item_id}").status_code == 204


def test_health(client: FlaskClient) -> None:
    assert client.get("/api/health").get_json()["status"] == "ok"


# ----------------------------------------------------------------- safety
def test_foreign_host_header_is_refused(client: FlaskClient) -> None:
    response = client.get("/", headers={"Host": "attacker.example"})
    assert response.status_code == 400


def test_cross_site_post_is_refused(client: FlaskClient) -> None:
    response = client.post(
        "/notes", data={"title": "x"}, headers={"Origin": "https://attacker.example"}
    )
    assert response.status_code == 403


def test_fetch_metadata_cross_site_is_refused(client: FlaskClient) -> None:
    for site in ["cross-site", "same-site"]:  # same-site = e.g. another port on localhost
        response = client.post("/notes", data={"title": "x"}, headers={"Sec-Fetch-Site": site})
        assert response.status_code == 403


def test_same_origin_post_is_allowed(client: FlaskClient) -> None:
    response = client.post("/notes", data={"title": "x"}, headers={"Origin": "http://localhost"})
    assert response.status_code == 302


# ----------------------------------------------------------------- export
def test_export_downloads(client: FlaskClient) -> None:
    make_note(client, title="t", items=["x"])
    as_json = client.get("/export.json")
    assert as_json.mimetype == "application/json"
    assert "attachment" in as_json.headers["Content-Disposition"]
    assert as_json.get_json()["notes"][0]["title"] == "t"
    as_md = client.get("/export.md")
    assert "- [ ] x" in as_md.get_data(as_text=True)
