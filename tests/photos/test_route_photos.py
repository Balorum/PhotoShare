from unittest.mock import MagicMock, patch
from PIL import Image
import io
import pytest

from fastapi import UploadFile
from src.database.models import User
from src.services.auth import auth_service


def create_file():
    file_data = io.BytesIO()
    image = Image.new("RGB", size=(100, 100), color=(255, 0, 0))
    image.save(file_data, "jpeg")
    file_data.seek(0)
    file = UploadFile(file_data)
    return file


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


def test_create_photo(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        data = {
            "title": "test_post",
            "description": "test_post",
            "tags": ["test_post"],
        }
        file = create_file()
        print(type(create_file))

        response = client.post(
            "/api/photos/create/",
            headers={"Authorization": f"Bearer {token}"},
            data=data,
            files={"file": ("test.jpg", file, "image/jpeg")},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["title"] == "test_photo"
        assert data["description"] == "lorem ipsum"
        assert isinstance(data["description"], str)
        assert "id" in data
