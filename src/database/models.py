import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    func,
    Table,
    Text,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(355), nullable=True)
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    role = Column(String(15))
    refresh_token = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    confirmed = Column(Boolean, default=False)


photo_m2m_tag = Table(
    "photo_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("photo_id", Integer, ForeignKey("photos.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    image_url = Column(String(500))
    title = Column(String(50), nullable=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    tags = relationship("Tag", secondary=photo_m2m_tag, backref="photos")
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user = relationship("User", backref="photos")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String(25), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )

    user = relationship("User", backref="tags")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None)
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    photo_id = Column(
        "photo_id", ForeignKey("photos.id", ondelete="CASCADE"), default=None
    )
    update_status = Column(Boolean, default=False)

    user = relationship("User", backref="comments")
    post = relationship("Photo", backref="comments")


class Blacklist(Base):
    __tablename__ = "blacklists"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
