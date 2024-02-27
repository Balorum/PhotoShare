import json
from unittest.mock import MagicMock
from datetime import datetime
import pytest

from src.database.models import User, Photo

from src.services.auth import auth_service


@pytest.mark.parametrize(
    "photo_id, user_id, result", [(1, 1, 200), (2, 2, 200)]  # own post  # another user
)
def test_create_post(session, photo_id, user_id, result):
    """
    The test_create_post function creates a new Post object and adds it to the database.
        Args:
            session (sqlalchemy.orm.sessionmaker): The SQLAlchemy session used for interacting with the database.
            post_id (int): The ID of the post being created in this function call, which is also its primary key in
                the database table that stores posts' information.
            user_id (int): The ID of the user who created this post, which is also its foreign key in
                the database table that stores posts' information.

    :param session: Create a post in the database
    :param post_id: Set the id of the post
    :param user_id: Create a user_id for the post
    :param result: Store the result of the test
    :return: The post object
    """
    test_post = Photo()
    test_post.id = photo_id
    test_post.image_url = "image_url"
    test_post.title = "title"
    test_post.description = "description"
    test_post.created_at = datetime.now()
    test_post.updated_at = datetime.now()
    test_post.user_id = user_id
    test_post.tags = []
    test_post.avg_rating = None

    session.add(test_post)
    session.commit()


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


@pytest.mark.parametrize(
    "photo_id, rate, result",
    [
        (1, 5, 423),  # Response [423 Locked]
        (2, 3, 200),  # Response [200]
        (3, 3, 404),  # Response [404]
    ],
)
def test_create_rating(session, client, token, photo_id, rate, result):
    response = client.post(
        f"api/ratings/create/{photo_id}/{rate}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == result


@pytest.mark.parametrize(
    "rate_id, new_rate, result", [(1, 5, 200), (2, 3, 404), (3, 3, 404)]
)
def test_edit_rating(session, client, token, rate_id, new_rate, result):
    response = client.put(
        f"api/ratings/edit/{rate_id}/{new_rate}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == result


@pytest.mark.parametrize("rate_id, result", [(1, 200), (2, 404), (3, 404)])
def test_delete_rating(session, client, token, rate_id, result):
    response = client.delete(
        f"api/ratings/delete/{rate_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == result


@pytest.mark.parametrize(
    "photo_id, rate, result",
    [
        (1, 5, 423),  # Response [423 Locked]
        (2, 3, 200),  # Response [200]
        (3, 3, 404),  # Response [404]
    ],
)
def test_create_rating_2(session, client, token, photo_id, rate, result):
    response = client.post(
        f"api/ratings/create/{photo_id}/{rate}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == result


def test_all_ratings(session, client, token):
    response = client.get(
        "api/ratings/all", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert type(response.json()) == list


def test_all_my_rates(session, client, token):
    response = client.get(
        "api/ratings/all_my", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert type(response.json()) == list


@pytest.mark.parametrize("user_id, photo_id, result", [(1, 2, 200), (1, 3, 404)])
def test_user_for_photo(session, client, token, user_id, photo_id, result):
    response = client.get(
        f"api/ratings/user_photo/{user_id}/{photo_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == result
