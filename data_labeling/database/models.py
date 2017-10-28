"""Module responsible for defining all of the relational database models"""
from flask_user import UserMixin
from sqlalchemy import Column, Integer, String

from data_labeling.database import Base


class User(Base, UserMixin):
    """Defines model for the Users table entry"""
    __tablename__ = 'Users'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    username: str = Column(String(50), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False, server_default='')

    def __init__(self, username: str, password_hash: str) -> None:
        self.username = username
        self.password = password_hash
