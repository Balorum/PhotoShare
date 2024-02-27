from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from faker import Faker
from main import app
from src.database.models import User
from test_db import get_db
from unittest.mock import MagicMock

client = TestClient(app)
fake = Faker()


def create_test_user(db: Session):
    user_data = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_comment():
    with TestClient(app) as client:
        # Arrange: Prepare test data
        db = next(get_db())
        user = create_test_user(db)

        # Create a MagicMock for the access token
        user.access_token = "mocked_access_token"

        # Assign the access token from the MagicMock
        client.headers["Authorization"] = f"Bearer {user.access_token}"

        # Act: Make the request to the endpoint
        # Your code for making the request and assertions goes here


def test_create_comment_invalid_input():
    with TestClient(app) as client:
        # Arrange: Prepare test data
        db = next(get_db())
        user = create_test_user(db)

        # Create a MagicMock for the access token
        user.access_token = "mocked_access_token"

        # Assign the access token from the MagicMock
        client.headers["Authorization"] = f"Bearer {user.access_token}"
        photo_id = 999  # Assuming this photo ID does not exist
        comment_data = {"text": "Test comment"}

        # Act: Make the request to the endpoint
        # Your code for making the request and assertions goes here


def test_edit_comment():
    with TestClient(app) as client:
        # Arrange: Prepare test data
        db = next(get_db())
        user = create_test_user(db)

        # Create a MagicMock for the access token
        user.access_token = "mocked_access_token"

        # Assign the access token from the MagicMock
        client.headers["Authorization"] = f"Bearer {user.access_token}"
        comment_id = 1
        new_text = "Updated test comment"

        # Act: Make the request to the endpoint
        # Your code for making the request and assertions goes here


def test_edit_comment_invalid_input():
    with TestClient(app) as client:
        # Arrange: Prepare test data
        db = next(get_db())
        user = create_test_user(db)

        # Create a MagicMock for the access token
        user.access_token = "mocked_access_token"

        # Assign the access token from the MagicMock
        client.headers["Authorization"] = f"Bearer {user.access_token}"
        comment_id = 999  # Assuming this comment ID does not exist
        new_text = "Updated test comment"

        # Act: Make the request to the endpoint
        # Your code for making the request and assertions goes here


# Write similar tests for other routes...
