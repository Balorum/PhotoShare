import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Comment
from src.repository.comments import (
    create_comment,
    get_comment,
    edit_comment,
    delete_comment,
)

# from asynctest import TestCase, CoroutineMock
import sys

# sys.path.append("../../src")


class TestCommentRepository(unittest.TestCase):

    def setUp(self):
        engine = create_engine("sqlite:///./test.db")
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    async def test_create_comment(self):
        db = self.Session()
        comment_data = {"text": "Test Comment"}
        photo_id = 1
        user_id = 1
        created_comment = await create_comment(db, comment_data, photo_id, user_id)
        self.assertIsNotNone(created_comment)
        self.assertEqual(created_comment.text, "Test Comment")
        db.close()

    async def test_get_comment(self):
        db = self.Session()
        comment_data = {"text": "Test Comment"}
        photo_id = 1
        user_id = 1
        created_comment = await create_comment(db, comment_data, photo_id, user_id)
        fetched_comment = await get_comment(db, created_comment.id)
        self.assertIsNotNone(fetched_comment)
        self.assertEqual(fetched_comment.text, "Test Comment")
        db.close()

    async def test_edit_comment(self):
        db = self.Session()
        comment_data = {"text": "Test Comment"}
        photo_id = 1
        user_id = 1
        created_comment = await create_comment(db, comment_data, photo_id, user_id)
        edited_comment = await edit_comment(
            db, created_comment.id, "Edited Test Comment"
        )
        self.assertIsNotNone(edited_comment)
        self.assertEqual(edited_comment.text, "Edited Test Comment")
        db.close()

    async def test_delete_comment(self):
        db = self.Session()
        comment_data = {"text": "Test Comment"}
        photo_id = 1
        user_id = 1
        created_comment = await create_comment(db, comment_data, photo_id, user_id)
        deleted_comment = await delete_comment(db, created_comment.id)
        self.assertIsNotNone(deleted_comment)
        self.assertEqual(deleted_comment.text, "Test Comment")
        db.close()


if __name__ == "__main__":
    unittest.main()
