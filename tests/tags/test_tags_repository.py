import pytest
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.schemas.photos import TagBase
from src.database.models import User, Tag
from src.services.auth import auth_service
from src.repository.tags import (
    create_tag,
    get_all_tags,
    update_tag,
    remove_tag,
)


class TestTags(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_all_tags(self):
        tags = [Tag(), Tag(), Tag()]
        self.session.query().offset().limit().all.return_value = tags
        result = await get_all_tags(skip=0, limit=10, user=1, db=self.session)
        self.assertEqual(result, tags)

    async def test_create_tag(self):
        tag = Tag(title="test")
        body = TagBase(title="test")
        self.session.query().filter().first.return_value = tag
        result = await create_tag(body=body, user=self.user, db=self.session)
        self.assertEqual(result.title, body.title)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_tag_found(self):
        tag = Tag()
        self.session.query().filter().first.return_value = tag
        result = await remove_tag(tag_id=1, user=self.user, db=self.session)
        self.assertEqual(result, tag)

    async def test_remove_tag_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_tag(tag_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_tag_found(self):
        body = Tag(title="test")
        self.session.query().filter().first.return_value = body
        result = await update_tag(tag_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, body)

    async def test_update_note_not_found(self):
        body = TagBase(title="test")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_tag(tag_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
