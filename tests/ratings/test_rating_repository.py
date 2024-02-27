from datetime import datetime

import pytest

from src.database.models import User, Photo, Rating
from src.repository import ratings as repository_ratings


@pytest.fixture()
def new_user(user, session):
    new_user = session.query(User).filter(User.email == user.get("email")).first()
    if new_user is None:
        new_user = User(
            email=user.get("email"),
            username=user.get("username"),
            password=user.get("password"),
            role=user.get("role"),
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user


@pytest.fixture()
def photo(session):
    photo = Photo(
        id=1,
        image_url="Column(String(300))",
        title="Column(String(50), nullable=True)",
        description="Column(String(500), nullable=True)",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user_id=3,
        tags=[],
    )
    session.add(photo)
    session.commit()
    session.refresh(photo)
    return photo


@pytest.fixture()
def rating(session):
    rating = Rating(id=1, rate=4, created_at=datetime.now(), photo_id=1, user_id=1)
    session.add(rating)
    session.commit()
    session.refresh(rating)
    return rating


@pytest.mark.asyncio
async def test_create_rate(photo, new_user, session):
    response = await repository_ratings.create_rate(1, 4, session, new_user)
    assert response.rate == 4
    assert response.user_id == 1
    assert response.photo_id == 1


@pytest.mark.asyncio
async def test_edit_rate(new_user, session):
    response = await repository_ratings.edit_rate(1, 5, session, new_user)
    assert response.rate == 5
    assert response.user_id == 1
    assert response.photo_id == 1


@pytest.mark.asyncio
async def test_delete_rate(new_user, session):
    response = await repository_ratings.delete_rate(1, session, new_user)
    assert response.rate == 5
    assert response.user_id == 1
    assert response.photo_id == 1


@pytest.mark.asyncio
async def test_show_ratings(rating, new_user, session):
    response = await repository_ratings.show_ratings(session, new_user)
    assert isinstance(response, list)
    assert response[0].rate == 4
    assert response[0].user_id == 1


@pytest.mark.asyncio
async def test_show_my_ratings(new_user, session):
    response = await repository_ratings.show_my_ratings(session, new_user)
    assert isinstance(response, list)


@pytest.mark.asyncio
async def test_user_rate_photo(new_user, session):
    response = await repository_ratings.user_rate_post(1, 1, session, new_user)
    assert response.rate == 4
    assert response.user_id == 1
    assert response.photo_id == 1
