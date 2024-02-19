# test_routes_comments.py

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.routes import comments
from src.database.models import Comment, User
from src.schemas.photos import CommentBase, CommentUpdate, CommentModel


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_auth_service():
    return MagicMock()


@pytest.fixture
def mock_current_user():
    return MagicMock(spec=User)


def test_create_comment(mock_db, mock_auth_service, mock_current_user):
    photo_id = 1
    comment_data = CommentBase(text="New comment")
    expected_comment = Comment(
        **comment_data.dict(), user_id=mock_current_user.id, post_id=photo_id
    )

    result = comments.create_comment(
        photo_id, comment_data, db=mock_db, current_user=mock_current_user
    )

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(expected_comment)
    assert result == expected_comment


def test_edit_comment(mock_db, mock_auth_service, mock_current_user):
    comment_id = 1
    new_text = "Updated comment"
    comment = Comment(id=comment_id, text="Old comment")
    mock_db.query().filter().first.return_value = comment

    result = comments.edit_comment(
        comment_id, new_text, db=mock_db, current_user=mock_current_user
    )

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(comment)
    assert comment.text == new_text
    assert result == {"message": "Comment updated successfully"}


def test_edit_comment_not_found(mock_db, mock_auth_service, mock_current_user):
    comment_id = 1
    new_text = "Updated comment"
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException):
        comments.edit_comment(
            comment_id, new_text, db=mock_db, current_user=mock_current_user
        )


def test_delete_comment(mock_db, mock_auth_service, mock_current_user):
    comment_id = 1
    comment = Comment(id=comment_id, text="Test comment")
    mock_db.query().filter().first.return_value = comment

    result = comments.delete_comment(
        comment_id, db=mock_db, current_user=mock_current_user
    )

    mock_db.delete.assert_called_once_with(comment)
    mock_db.commit.assert_called_once()
    assert result == comment


def test_delete_comment_not_found(mock_db, mock_auth_service, mock_current_user):
    comment_id = 1
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException):
        comments.delete_comment(comment_id, db=mock_db, current_user=mock_current_user)
