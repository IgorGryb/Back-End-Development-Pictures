"""PyTest suite for the Pictures microservice (IBM Back-End Development Capstone)."""
import pytest
from app import app, pictures


@pytest.fixture(autouse=True)
def reset_store():
    # reset the in-memory store before every test for isolation
    pictures.clear()
    pictures[1] = {"id": 1, "title": "Sunset over the lake",
                   "url": "https://example.com/pics/sunset.jpg"}
    pictures[2] = {"id": 2, "title": "City skyline at night",
                   "url": "https://example.com/pics/city.jpg"}
    import app as appmod
    appmod._next_id = 3
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------- Exercise 1: health + count ----------
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "OK"


def test_count(client):
    resp = client.get("/pictures/count")
    assert resp.status_code == 200
    assert resp.get_json()["count"] == 2


# ---------- Exercise 2: Get Pictures (5 tests) ----------
def test_get_pictures_returns_list(client):
    resp = client.get("/pictures")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_picture_by_id(client):
    resp = client.get("/pictures/1")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Sunset over the lake"


def test_get_picture_returns_all_fields(client):
    resp = client.get("/pictures/2")
    pic = resp.get_json()
    assert set(pic.keys()) == {"id", "title", "url"}
    assert pic["id"] == 2


def test_get_picture_not_found(client):
    resp = client.get("/pictures/999")
    assert resp.status_code == 404


def test_get_pictures_content_type_json(client):
    resp = client.get("/pictures")
    assert resp.content_type == "application/json"


# ---------- Exercise 4: POST picture ----------
def test_post_picture_creates(client):
    resp = client.post("/pictures", json={"title": "Mountain trail",
                                          "url": "https://example.com/pics/mountain.jpg"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] == 3
    assert body["title"] == "Mountain trail"


def test_post_picture_increases_count(client):
    client.post("/pictures", json={"title": "Beach", "url": "https://example.com/pics/beach.jpg"})
    assert client.get("/pictures/count").get_json()["count"] == 3


def test_post_picture_missing_fields_returns_400(client):
    resp = client.post("/pictures", json={"title": "No URL"})
    assert resp.status_code == 400


# ---------- Exercise 6: update / delete ----------
def test_put_picture_updates_title(client):
    resp = client.put("/pictures/1", json={"title": "Sunset, remastered"})
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Sunset, remastered"
    assert client.get("/pictures/1").get_json()["title"] == "Sunset, remastered"


def test_put_picture_not_found(client):
    assert client.put("/pictures/999", json={"title": "x"}).status_code == 404


def test_delete_picture_removes_it(client):
    resp = client.delete("/pictures/2")
    assert resp.status_code == 200
    assert client.get("/pictures/2").status_code == 404
    assert client.get("/pictures/count").get_json()["count"] == 1


def test_delete_picture_not_found(client):
    assert client.delete("/pictures/999").status_code == 404
