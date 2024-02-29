# from unittest.mock import MagicMock, patch
# from PIL import Image
# import io
# import pytest

# from fastapi import File
# from src.database.models import User
# from src.services.auth import auth_service


# @pytest.fixture()
# def token(client, user, session, monkeypatch):
#     mock_send_email = MagicMock()
#     monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
#     client.post("/api/auth/signup", json=user)
#     current_user: User = (
#         session.query(User).filter(User.email == user.get("email")).first()
#     )
#     current_user.confirmed = True
#     session.commit()
#     response = client.post(
#         "/api/auth/login",
#         data={"username": user.get("email"), "password": user.get("password")},
#     )
#     data = response.json()
#     return data["access_token"]


# def test_get_transform_url(client, token):
#     data = {
#         "height": 0,
#         "width": 0,
#         "crop": "fill",
#         "blur": 100,
#         "angle": 0,
#         "opacity": 100
#     }
#     response = client.post("/api/transforms/get_transform/1", data=data, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 201, response.text


# def test_get_qr(client, token):
#     response = client.get("/api/transforms/")
