# test_repository_comments.py

import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.repository import comments
from src.database.models import Comment
from src.schemas.photos import CommentBase


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


def test_show_comment(mock_session):
    comment_id = 1
    comment = Comment(id=comment_id, text="Test comment")
    mock_session.query().filter().first.return_value = comment

    result = comments.show_comment(mock_session, comment_id)

    assert result == comment


def test_create_comment(mock_session):
    user_id = 1
    photo_id = 1
    comment_data = CommentBase(text="New comment")
    expected_comment = Comment(**comment_data.dict(), user_id=user_id, post_id=photo_id)

    result = comments.create_comment(mock_session, comment_data, user_id, photo_id)

    mock_session.add.assert_called_once_with(expected_comment)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(expected_comment)
    assert result == expected_comment


def test_edit_comment(mock_session):
    comment_id = 1
    new_text = "Updated comment"
    comment = Comment(id=comment_id, text="Old comment")
    mock_session.query().filter().first.return_value = comment

    result = comments.edit_comment(mock_session, comment_id, new_text)

    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(comment)
    assert comment.text == new_text
    assert result == comment


def test_delete_comment(mock_session):
    comment_id = 1
    comment = Comment(id=comment_id, text="Test comment")
    mock_session.query().filter().first.return_value = comment

    comments.delete_comment(mock_session, comment_id)

    mock_session.delete.assert_called_once_with(comment)
    mock_session.commit.assert_called_once()
