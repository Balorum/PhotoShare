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
from src.repository.photos import (
    get_photos,
    get_user_photos,
    get_photo,
    get_photo_by_id,
    create_photo,
    remove_photo,
    update_photo,
)


def create_file():
    file_data = io.BytesIO()
    image = Image.new("RGB", size=(100, 100), color=(255, 0, 0))
    image.save(file_data, "jpeg")
    file_data.seek(0)
    return file_data


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(
            id=1, username="test_user", password="qwerty", confirmed=True, role="user"
        )

    async def test_get_photos(self):
        photos = [Photo(), Photo(), Photo()]
        self.session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
            photos
        )
        result = await get_photos(10, 0, self.session)
        self.assertEqual(result, photos)

    async def test_get_user_photos(self):
        photos = [Photo(user_id=1), Photo(user_id=1), Photo()]
        self.session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = (
            photos
        )
        result = await get_user_photos(10, 0, self.user, self.session)
        self.assertEqual(result, photos)

    async def test_get_photo(self):
        photo = Photo(id=1)
        self.session.query.return_value.filter.return_value.first.return_value = photo
        result = await get_photo(1, self.user, self.session)
        self.assertEqual(result, photo)

    async def test_get_photo_not_found(self):
        self.session.query.return_value.filter.return_value.first.return_value = None
        result = await get_photo(1, self.user, self.session)
        self.assertIsNone(result)

    async def test_get_photo_by_id(self):
        self.user.role = "admin"
        photo = Photo(id=1, user_id=1)
        self.session.query.return_value.filter.return_value.first.return_value = photo
        result = await get_photo_by_id(1, self.user, self.session)
        self.assertEqual(result, photo)
        self.user.role = "user"
        photo = Photo(id=1, user_id=2)
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            photo
        )
        result = await get_photo_by_id(1, self.user, self.session)
        self.assertEqual(result, photo)

    async def test_create_photo(self):
        title = "photo_title"
        description = "photo_description"
        tags = ["test_tag1", "test_tag2", "test_tag3"]
        file = create_file()

        result = await create_photo(
            title, description, tags, self.user, file, self.session
        )
        assert isinstance(result.image_url, str)
        assert result.title == title
        assert result.description == description

    async def test_update_photo(self):
        id = 1
        user_id = 1
        title = "photo_title"
        description = "photo_description"
        tags = []
        image_url = "photo_file"
        file = create_file()

        result = await update_photo(
            id,
            title,
            description,
            tags,
            self.user,
            file,
            self.session,
        )
        assert isinstance(result.image_url, str)
        assert image_url != result.image_url
        assert result.title == title
        assert result.description == description

    async def test_delete_photo_by_id(self):
        photo = Photo(id=1, user_id=1)
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            photo
        )
        result = await remove_photo(1, self.user, self.session)
        self.assertEqual(result, photo)
