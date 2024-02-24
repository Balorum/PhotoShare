import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database.models import Comment, User
from src.repository import comments
from tests.utils import generate_comment, generate_user


@pytest.mark.asyncio
async def test_create_comment(db_session: Session):
    sample_user = await create_sample_user(db_session)
    comment_data = {
        "text": "Test comment",
    }
    photo_id = 1
    user_id = sample_user.id
    comment = await comments.create_comment(db_session, comment_data, photo_id, user_id)
    assert comment is not None
    assert comment.text == comment_data["text"]
    assert comment.photo_id == photo_id
    assert comment.user_id == user_id
    assert comment.created_at is not None
    assert comment.updated_at is not None
    assert comment.update_status is True


@pytest.mark.asyncio
async def test_create_comment_invalid_data(db_session: Session):
    sample_user = await create_sample_user(db_session)
    invalid_comment_data = [
        {"text": ""},  # пустий текст коментаря
        {"text": " " * 1001},  # текст коментаря з більшою ніж допустима довжина
        {"text": None},  # нульове значення тексту коментаря
        # Тут можна додати інші неприпустимі варіанти даних
    ]
    photo_id = 1
    user_id = sample_user.id
    for data in invalid_comment_data:
        with pytest.raises(ValueError):
            await comments.create_comment(db_session, data, photo_id, user_id)


@pytest.mark.asyncio
async def test_get_comment(db_session: Session, sample_comment: Comment):
    comment_id = sample_comment.id
    retrieved_comment = await comments.get_comment(db_session, comment_id)
    assert retrieved_comment is not None
    assert retrieved_comment.id == sample_comment.id


@pytest.mark.asyncio
async def test_get_comment_photo_user_id(db_session: Session, sample_comment: Comment):
    photo_id = sample_comment.photo_id
    user_id = sample_comment.user_id
    retrieved_comment = await comments.get_comment_photo_user_id(
        db_session, photo_id, user_id
    )
    assert retrieved_comment is not None
    assert retrieved_comment.photo_id == photo_id
    assert retrieved_comment.user_id == user_id


@pytest.mark.asyncio
async def test_get_comment_photo_id(db_session: Session, sample_comment: Comment):
    photo_id = sample_comment.photo_id
    retrieved_comment = await comments.get_comment_photo_id(db_session, photo_id)
    assert retrieved_comment is not None
    assert retrieved_comment.photo_id == photo_id


@pytest.mark.asyncio
async def test_edit_comment(db_session: Session, sample_comment: Comment):
    new_text = "Updated comment"
    updated_comment = await comments.edit_comment(
        db_session, sample_comment.id, new_text
    )
    assert updated_comment is not None
    assert updated_comment.text == new_text
    assert updated_comment.updated_at is not None
    assert updated_comment.update_status is True


@pytest.mark.asyncio
async def test_delete_comment(db_session: Session, sample_comment: Comment):
    deleted_comment = await comments.delete_comment(db_session, sample_comment.id)
    assert deleted_comment is not None
    assert deleted_comment.id == sample_comment.id


async def create_sample_user(db_session: Session) -> User:
    user = generate_user()
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.fixture
async def sample_comment(db_session: Session):
    sample_user = await create_sample_user(db_session)
    photo_id = 1
    comment = generate_comment(sample_user.id, photo_id)
    db_session.add(comment)
    await db_session.commit()
    return comment
