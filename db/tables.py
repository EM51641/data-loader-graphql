"""
table users:
id - primary key
username : str
email


table posts:
id - primary key
title:str
content:text
user_id -> users.id

"""

from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.utils import Base


class BaseEntity(Base):  # type: ignore[name-defined]
    """
    Base model for all models.
    """

    __abstract__ = True


class PostEntity(BaseEntity):
    """
    Post model
    """

    __tablename__ = "posts"
    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    title: Mapped[String] = mapped_column(String(), nullable=False)
    content: Mapped[Text] = mapped_column(Text(), nullable=False)
    user_id: Mapped[Integer] = mapped_column(Integer(), ForeignKey("users.id"))
    user: Mapped["UserEntity"] = relationship("UserEntity", backref="posts")

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"<User {self.title}>"


class UserEntity(BaseEntity):
    """
    User model
    """

    __tablename__ = "users"
    id: Mapped[Integer] = mapped_column(Integer(), primary_key=True)
    username: Mapped[String] = mapped_column(String(45), nullable=False)
    email: Mapped[String] = mapped_column(String(80), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User {self.username}>"
