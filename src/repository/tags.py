from typing import List

from sqlalchemy.orm import Session

from src.database.models import Tag, User
from src.schemas.photos import TagBase


async def get_my_tags() -> List[Tag]:
    pass

async def create_tag() -> Tag:
    pass


async def get_all_tags() -> List[Tag]:
    pass


async def update_tag() -> Tag | None:
    pass


async def remove_tag() -> Tag | None:
    pass



