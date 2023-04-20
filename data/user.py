"""py-file with the mechanism of the db-table 'user'"""


from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm, Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """class of the table 'user'
        contains next fields:
        id - unique key integer
        nick - string, nickname of the user
        email - string, must be unique
        hashed_psw - string, hashed password
        words - words with user_id=user.id
        dicts - dictionaries with user_id=user.id"""
    __tablename__ = 'user'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    nick = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_psw = Column(String, nullable=False)
    words = orm.relationship('Word', back_populates='user')
    dicts = orm.relationship('Dict', back_populates='user')

    def __repr__(self):
        return f'User(id={self.id}, email="{self.email}")'

    def set_psw(self, psw):
        """setting password psw"""
        self.hashed_psw = generate_password_hash(psw)

    def check_psw(self, psw):
        """function for checking of the equality of the given password psw and current password
        returns True if they are equal"""
        return check_password_hash(self.hashed_psw, psw)
