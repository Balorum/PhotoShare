from unittest.mock import MagicMock, patch

import pytest

from src.database.models import User, Tag
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = (
        session.query(User).filter(User.email == user.get("email")).first()
    )
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def tag(user, token, session):
    """
    The tag function takes in a user, token, and session.
    It then queries the database for the current user and hashtag.
    If there is no hashtag it creates one with a title of dog and adds it to the database.

    :param user: Get the user id from the database
    :param token: Authenticate the user
    :param session: Query the database
    :return: An object of type hashtag, which is a sqlalchemy model
    """
    cur_user = session.query(User).filter(User.email == user["email"]).first()
    tag = session.query(Tag).first()
    if tag is None:
        tag = Tag(title="dog", user_id=cur_user.id)
        session.add(tag)
        session.commit()
        session.refresh(tag)
    return tag


@pytest.fixture()
def body():
    return {"title": "string"}


def test_create_tag(body, client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            f"/api/tags/create/",
            json=body,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data.get("title") is not None


def test_get_all_tags(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            f"/api/tags/all/", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["title"] == "string"
        assert "id" in data[0]


def test_read_tag_by_id(tag, client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            f"/api/tags/by_id/{tag.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "string"
        assert "id" in data


def test_get_tag_not_found(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/tags/2", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_update_tag(tag, client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            f"/api/tags/change_tag/{tag.id}",
            json={"title": "new_test_tag"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "new_test_tag"
        assert "id" in data


def test_update_tag_not_found(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/tags/2",
            json={"title": "new_test_tag"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"


def test_delete(tag, client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            f"/api/tags/del/{tag.id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "new_test_tag"
        assert "id" in data


def test_repeat_delete_tag(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/tags/1", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"
