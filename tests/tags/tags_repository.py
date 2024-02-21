import pytest
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.schemas.photos import TagBase
from src.database.models import User, Tag
from src.services.auth import auth_service
from src.repository.tags import (
    get_my_tags,
    create_tag,
    get_all_tags,
    update_tag,
    remove_tag,
)


# class TestTags(unittest.IsolatedAsyncioTestCase):

#     def setUp(self):
#         self.session = MagicMock(spec=Session)
#         self.user = User(id=1)

    # async def test_get_all_tags(self):
    #     tags = [Tag(), Tag(), Tag()]
    #     self.session.query().filter().offset().limit().all.return_value = tags
    #     result = await get_all_tags(skip=0, limit=10, user=1, db=self.session)
    #     self.assertEqual(result, tags)

    # async def test_create_tag(self):
    #     body = TagBase(title="test")
    #     result = await create_tag(body=body, user=self.user, db=self.session)
    #     self.assertEqual(result.title, body.title)
    #     self.assertTrue(hasattr(result, "id"))




if __name__ == '__main__':
    unittest.main()