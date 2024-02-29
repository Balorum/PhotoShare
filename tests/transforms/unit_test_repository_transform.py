import collections
import pathlib
from PIL import Image
import io

collections.Callable = collections.abc.Callable
import unittest
from unittest.mock import MagicMock
from fastapi import UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from src.database.models import Photo, User, Tag
from src.schemas.transform import TransformModel
from src.repository.transforms import (

    get_transform_url,
    get_qr_code
)
from src.repository.photos import create_photo


def create_file():
    file_data = io.BytesIO()
    image = Image.new("RGB", size=(100, 100), color=(255, 0, 0))
    image.save(file_data, "jpeg")
    file_data.seek(0)
    file = UploadFile(file_data)
    return file


class TestRouteTransform(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(
            id=1, username="test_user", password="qwerty", confirmed=True, role="user"
        )

    async def test_get_transform_url(self):
        title = "photo_title"
        description = "photo_description"
        tags = ["test_tag1", "test_tag2", "test_tag3"]
        file = create_file()

        result = await create_photo(
            title, description, tags, self.user, file, self.session
        )
        result.id = 1
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            result
        )
        transform_url = 'https://res.cloudinary.com/dmbcwijhm/image/upload/c_fill,h_250,w_250/e_blur:100/a_0/o_100/v1709145575/PhotoShareApp/transform/test_user'
        transform = TransformModel(height=250, width=250)
        result2 = await get_transform_url(1, transform, self.user, self.session)
        self.assertEqual(transform_url, result2)

    async def test_get_transform_url_not_found(self):
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            None
        )
        transform = TransformModel(height=250, width=250)
        result = await get_transform_url(1, transform, self.user, self.session)
        self.assertIsNone(result)

    async def test_get_qr_code(self):
        title = "photo_title"
        description = "photo_description"
        tags = ["test_tag1", "test_tag2", "test_tag3"]
        file = create_file()

        result = await create_photo(
            title, description, tags, self.user, file, self.session
        )
        result.id = 1
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            result
        )
        qr_url = 'https://res.cloudinary.com/dmbcwijhm/image/upload/h_250,w_250/v1709146496/PhotoShareApp/qrcode/test_user'
        result_qr = await get_qr_code(1, self.user, self.session)
        self.assertEqual(result_qr, qr_url)

    async def test_get_qr_code_not_found(self):
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            None
        )
        result_qr = await get_qr_code(1, self.user, self.session)
        self.assertIsNone(result_qr)


if __name__ == "__main__":
    unittest.main()
