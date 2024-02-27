import unittest
from unittest.mock import MagicMock
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.schemas.users import UserModel, UserDb, UserProfileModel
from src.database.models import User, Role
from src.repository.users import (
    ban_user,
    change_user_role,
    confirmed_email, 
    create_user, 
    delete_user,
    get_me, 
    get_user_by_email, 
    get_users, 
    get_user_profile, 
    remove_from_ban,
    update_avatar,
    update_token
)

class TestUsersRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

   
    async def test_get_me(self):
        id = 1
        username = 'Michael'
        email = "test_email@api.com"
        user = User(email=email, id=id)
        self.session.query().filter().first.return_value= user

        result = await get_me(user, db=self.session)
        self.assertEqual(result, user)


    async def test_get_user_by_email(self):
        email = "test_email@api.com"
        user = User(id=1,  email=email)
        self.session.query().filter().first.return_value = user  

        result = await get_user_by_email(email=email, db=self.session)
        self.assertEqual(result, user)    


    async def test_get_user_by_email_nonexistent(self):
        email = "noт_existent_email@api.com"
        self.session.query().filter().first.return_value = None  

        result = await get_user_by_email(email=email, db=self.session)
        self.assertIsNone(result)


    async def test_create_user(self):
                       
        data = UserModel(username="Michael", email="test@api.com", password="qwerty")

        result = await create_user(body=data, db=self.session)
        self.assertEqual(result.username, data.username)
        self.assertEqual(result.email, data.email)
        self.assertEqual(result.password, data.password)


    async def test_update_token(self):
        user = User(id=1,  email="test_email@api.com")
        token = "new_refresh_token"
        self.session.commit.return_value = None
       
        await update_token(user=user, token=token, db=self.session)
        self.assertEqual(user.refresh_token, token)

    async def test_update_avatar(self):
        user_email = "test_email@api.com"
        avatar_url = "https://fake.com/avatar.png"
        user = User(avatar=avatar_url)
        self.session.commit.return_value = None

        updated_user = await update_avatar(email=user_email, url=avatar_url, db=self.session)
        self.assertEqual(updated_user.avatar, user.avatar)    


    async def test_confirmed_email(self):
        user_email = "test_email@api.com"
        user = User(id=1,  email=user_email, confirmed=True)
        self.session.commit.return_value = None
   
        await confirmed_email(email=user_email, db=self.session)
        self.assertTrue(user.confirmed)


    async def test_get_users(self):
        users = [User(), User(), User()]
        self.session.query().offset().limit().all.return_value = users
        
        result = await get_users(skip=0, limit=10, db=self.session)
        self.assertEqual(result, users)


    async def test_get_user_profile(self):
        email = "test_уmail@api.com"
        username = "Michael"
        created_at=datetime.now()
        user = User(username = username, email = email, created_at=created_at)
        self.session.query().filter().first.return_value = user
        photo_count = 5
        self.session.query().filter().count.return_value = photo_count
        comment_count = 5
        self.session.query().filter().count.return_value = comment_count
       
        result = await get_user_profile(username=username, db=self.session)
      
        assert isinstance(result, UserProfileModel)
        self.assertEqual(result.username, user.username)
        self.assertEqual(result.email, user.email)


    async def test_get_user_profile_nonexistent(self):
        email = "test_уmail@api.com"
        username = "Michael"
        created_at=datetime.now()
        user = User(username = username, email = email, created_at=created_at)
        self.session.query().filter().first.return_value  = None
        result = await get_user_profile(username=username, db=self.session)
        self.assertIsNone(result)    


    async def test_change_user_role(self):
        user_email = "test_email@api.com"
        role = Role.admin
        user = User(role=role, email=user_email)
        
        self.session.scalar.return_value = user
        
        await change_user_role(user_email, role, self.session)
        self.assertEqual(user.role, role)


    async  def test_ban_user(self):
        user_email = "test_email@api.com"
        is_active = True
        user = User(is_active=is_active)
        self.session.query().filter().first.return_value = user
        
        result = await ban_user(user_email, db=self.session)
        print(user.is_active)
        self.assertFalse(user.is_active)


    async def test_remove_from_ban(self):
        user_email = "test_email@api.com"
        is_active = False
        user = User(is_active=is_active)
        self.session.query().filter().first.return_value = user
       
        await remove_from_ban(email=user_email, db=self.session) 
        print(user.is_active)
        self.assertTrue(user.is_active)


    async def test_delete_user(self):
        user_id = 1
        user = User(id=1)
        self.session.query().filter_by().first.return_value = user
        self.session.commit.return_value = None

        result = await delete_user(user_id=user_id, db=self.session)
        self.assertEqual(result, user)   

if __name__ == '__main__':
    unittest.main()


