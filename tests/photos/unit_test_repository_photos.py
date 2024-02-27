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
from src.database.models import Photo, User
from src.schemas.photos import PhotoBase
from src.repository.photos import (
    get_photos,
    get_user_photos,
    get_photo,
    get_photo_by_id,
    create_photo,
    remove_photo,
    update_photo
)


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True, role='user')

    async def test_get_photos(self):
        photos = [Photo(), Photo(), Photo()]
        self.session.query.return_value.offset.return_value.limit.return_value.all.return_value = photos
        result = await get_photos(10, 0, self.session)
        self.assertEqual(result, photos)

    async def test_get_user_photos(self):
        photos = [Photo(user_id=1), Photo(user_id=1), Photo()]
        self.session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = photos
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
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = photo
        result = await get_photo_by_id(1, self.user, self.session)
        self.assertEqual(result, photo)

    # async def test_create_photo(self):
    #     title = 'photo_title'
    #     description = 'photo_description'
    #     file = 'photo_file'
    #     photo = Photo(title=title, description=description)
    #     result = await create_photo(title, description, None, self.user, file, self.session)
    #     self.assertEqual(result, photo)

    # async def test_update_contact(self):
    #     photo = Photo(id=1, user_id=1, title='photo_title', description='photo_description', image_url = 'photo_file')
    #     self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = Photo(id=1,
    #                                                                                                        user_id=1,
    #                                                                                                        title='photo_2',
    #                                                                                                        description='23131')
    #     result = await update_photo(photo.id, photo.title, photo.description, None, self.user, None, self.session)
    #     self.assertEqual(photo,result)
    async def test_delete_photo_by_id(self):
        photo = Photo(id=1, user_id=1)
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = photo
        result = await remove_photo(1, self.user, self.session)
        self.assertEqual(result, photo)
