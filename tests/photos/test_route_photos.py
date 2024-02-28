from datetime import datetime

import io
import pytest
from unittest.mock import MagicMock, patch
from PIL import Image

from src.database.models import User, Photo
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
def photo(user, token, session):

    cur_user = session.query(User).filter(User.email == user["email"]).first()
    photo = session.query(Photo).first()
    if photo is None:
        photo = Photo(
            image_url="https://res.cloudinary.com/dybgf2pue/image/upload/c_fill,h_250,w_250/Dominic",
            title="cat",
            description="pet",
            tags=["cat"],
            created_at=datetime.now(),
            user_id=cur_user.id,
        )
        session.add(photo)
        session.commit()
        session.refresh(photo)
    return photo


@pytest.fixture()
def new_user(user, token, session):

    new_user = session.query(User).filter(User.email == user.get("email")).first()
    if new_user is None:
        new_user = User(
            email=user.get("email"),
            username=user.get("username"),
            password=user.get("password"),
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user


def test_create_photo(client, token):

    file_data = io.BytesIO()
    image = Image.new("RGB", size=(100, 100), color=(255, 0, 0))
    image.save(file_data, "jpeg")
    file_data.seek(0)
    data = {"title": "test_photo", "description": "test_photo", "tags": ["test_photo"]}
    response = client.post(
        "/api/photos/create/",
        headers={"Authorization": f"Bearer {token}"},
        data=data,
        files={"file": ("test.jpg", file_data, "image/jpeg")},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "test_photo"
    assert data["description"] == "test_photo"
    assert isinstance(data["image_url"], str)
    assert "id" in data


def test_get_photos_by_user_id(new_user, client, token):

    response = client.get(
        f"/api/photos/get_by_user/{new_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["title"] == "test_photo"
    assert data[0]["description"] == "test_photo"


def test_get_all_posts(client, token):

    response = client.get(
        f"/api/photos/all/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["title"] == "test_photo"
    assert "id" in data[0]


def test_get_post_by_id(photo, client, token):

    response = client.get(
        f"/api/photos/by_id/{photo.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "test_photo"
    assert "id" in data


def test_get_post_by_id_not_found(photo, client, token):

    response = client.get(
        f"/api/photos/by_id/{photo.id+1}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not Found"


def test_get_photos(client, token):

    response = client.get(
        "/api/photos/all", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_photo(photo, client, token):

    response = client.put(
        f"/api/photos/{photo.id}",
        json={
            "title": "test_photo",
            "description": "test_photo",
            "tags": ["test_photo"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "test_photo"
    assert data["description"] == "test_photo"
    assert "id" in data


def test_update_photo_not_found(photo, client, token):

    response = client.put(
        f"/api/photos/{photo.id +1}",
        json={
            "title": "test_photo",
            "description": "test_photo",
            "tags": ["test_photo"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not Found"


def test_delete_post(photo, client, token):

    response = client.delete(
        f"/api/photos/{photo.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "test_photo"
    assert data["description"] == "test_photo"
    assert "id" in data


def test_repeat_delete_post(client, token):

    response = client.delete(
        f"/api/photos/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not Found"
