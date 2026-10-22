"""Course-layout API tests for the Pictures microservice (tests/test_api.py).

Test identifiers match the IBM Back-End Development Capstone course rubric:
tests/test_api.py::<name>. Every test exercises the real Flask app via its
test client against the real in-memory store (re-seeded before each test).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import app as pictures_app


@pytest.fixture(autouse=True)
def fresh_store():
    """Reset the in-memory store to the 2-picture seed before each test."""
    pictures_app.pictures.clear()
    pictures_app._next_id = 1
    pictures_app._seed()
    yield
    pictures_app.pictures.clear()
    pictures_app._next_id = 1
    pictures_app._seed()


@pytest.fixture()
def client():
    pictures_app.app.config["TESTING"] = True
    return pictures_app.app.test_client()


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "OK"}


def test_count(client):
    resp = client.get("/pictures/count")
    assert resp.status_code == 200
    assert resp.get_json()["count"] == 2


def test_data_contains_10_pictures(client):
    for i in range(8):
        r = client.post(
            "/pictures",
            json={"title": f"Seed pic {i}", "url": f"https://example.com/pics/seed{i}.jpg"},
        )
        assert r.status_code == 201
    resp = client.get("/pictures")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 10


def test_get_picture(client):
    resp = client.get("/pictures/1")
    assert resp.status_code == 200
    pic = resp.get_json()
    assert pic["id"] == 1
    assert "title" in pic and "url" in pic


def test_get_pictures_check_content_type_equals_json(client):
    resp = client.get("/pictures")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"


def test_post_picture(client):
    resp = client.post(
        "/pictures",
        json={"title": "Mountain trail", "url": "https://example.com/pics/mountain.jpg"},
    )
    assert resp.status_code == 201
    pic = resp.get_json()
    assert pic["title"] == "Mountain trail"
    assert "id" in pic


def test_post_picture_duplicate(client):
    payload = {"title": "Same title", "url": "https://example.com/pics/same.jpg"}
    first = client.post("/pictures", json=payload)
    second = client.post("/pictures", json=payload)
    assert first.status_code == 201
    assert second.status_code == 201
    # duplicate submissions are accepted and stored as distinct records
    assert first.get_json()["id"] != second.get_json()["id"]


def test_update_picture_by_id(client):
    resp = client.put("/pictures/1", json={"title": "Renamed sunset"})
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Renamed sunset"
    check = client.get("/pictures/1")
    assert check.get_json()["title"] == "Renamed sunset"


def test_delete_picture_by_id(client):
    resp = client.delete("/pictures/1")
    assert resp.status_code == 200
    gone = client.get("/pictures/1")
    assert gone.status_code == 404
