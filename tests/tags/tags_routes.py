import pytest
from unittest.mock import MagicMock, patch

from src.database.models import User, Hashtag
from ..src.services.auth import auth_service


def test_create_tag(client, token):
    with patch.object(auth_service, "r") as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/tags",
            json={"name": "test_tag"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["name"] == "test_tag"
        assert "id" in data
