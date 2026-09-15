import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.storage import authors, posts, comments, likes

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear():
    authors.clear()
    posts.clear()
    comments.clear()
    likes.clear()

def test_create_author():
    r = client.post("/authors", json={
        "name": "John Doe",
        "email": "john@example.com"
    })
    assert r.status_code == 200

def test_create_post():
    a = client.post("/authors", json={
        "name": "Jane",
        "email": "jane@example.com"
    }).json()
    r = client.post("/posts", json={
        "title": "Hello World",
        "content": "This is my first post",
        "author_id": a["id"]
    })
    assert r.status_code == 200
    assert r.json()["published"] == False

def test_publish_post():
    a = client.post("/authors", json={
        "name": "Test",
        "email": "test@test.com"
    }).json()
    p = client.post("/posts", json={
        "title": "Draft",
        "content": "Content here",
        "author_id": a["id"]
    }).json()
    r = client.post(f"/posts/{p['id']}/publish")
    assert r.json()["published"] == True
def test_like_post():
    a = client.post("/authors", json={"name": "Jane", "email": "jane@example.com"}).json()
    p = client.post("/posts", json={"title": "Hello World", "content": "This is my first post", "author_id": a["id"]}).json()
    r = client.post(f"/posts/{p['id']}/like", json={"user_name": "tester"})
    assert r.status_code == 200
    assert r.json()['message'] == "Post liked"


def test_count_likes():
    a = client.post("/authors", json={"name": "Jane", "email": "jane@example.com"}).json()
    p = client.post("/posts", json={"title": "Hello World", "content": "This is my first post", "author_id": a["id"]}).json()
    client.post(f"/posts/{p['id']}/like", json={"user_name": "tester1"})
    client.post(f"/posts/{p['id']}/like", json={"user_name": "tester2"})
    r = client.get(f"/posts/{p['id']}/likes")
    assert r.status_code == 200
    assert r.json()['like_count'] == 2


def test_invalid_post_like():
    r = client.post("/posts/invalid_id/like", json={"user_name": "tester"})
    assert r.status_code == 404


def test_invalid_post_like_count():
    r = client.get("/posts/invalid_id/likes")
    assert r.status_code == 404
