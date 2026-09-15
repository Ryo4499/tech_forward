import uuid
import time
from datetime import timedelta
from flask_jwt_extended import create_access_token


def test_article_lifecycle(app):
    client = app.test_client()

    def request(method, path, **kwargs):
        time.sleep(0.3)
        return client.open(path, method=method, **kwargs)

    name = "Test" + uuid.uuid4().hex[:12]
    registration = request(
        "POST",
        "/api/user",
        json={
            "userName": name,
            "email": "test@example.com",
            "password": "Testpassword12",
        },
    )
    assert registration.status_code == 201
    other = request(
        "POST",
        "/api/user",
        json={
            "userName": name + "Other",
            "email": "other@example.com",
            "password": "Testpassword12",
        },
    )
    assert other.status_code == 201
    login = request(
        "POST", "/api/login", json={"userName": name, "password": "Testpassword12"}
    )
    assert login.status_code == 200
    headers = {"Authorization": "Bearer " + login.json["access_token"]}
    assert (
        request(
            "DELETE", "/api/user/" + other.json["userId"], headers=headers
        ).status_code
        == 403
    )
    created = request(
        "POST",
        "/api/article",
        headers=headers,
        json={"title": "Original title", "content": "Original content", "draft": False},
    )
    assert created.status_code == 201
    path = "/api/article/" + created.json["articleId"]
    updated = request(
        "PUT",
        path,
        headers=headers,
        json={"title": "Updated title", "content": "Updated content", "draft": False},
    )
    assert updated.status_code == 200
    assert request("GET", path, headers=headers).json["content"] == "Updated content"
    assert request("DELETE", path, headers=headers).status_code == 200
    assert request("GET", path, headers=headers).status_code == 404
    assert request("POST", "/api/logout", headers=headers).status_code == 200
    assert request("GET", "/api/user/me", headers=headers).status_code == 401
    with app.app_context():
        expired = create_access_token(
            identity=registration.json["userId"], expires_delta=timedelta(seconds=-1)
        )
    assert (
        request(
            "GET", "/api/user/me", headers={"Authorization": "Bearer " + expired}
        ).status_code
        == 401
    )
