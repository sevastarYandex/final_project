import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    nick = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_psw = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    words = orm.relationship('Word', back_populates='user')
    dictionaries = orm.relationship('Dictionary', back_populates='user')

    def __repr__(self):
        return f'User(id={self.id}, email="{self.email}")'

    def set_psw(self, psw):
        self.hashed_psw = generate_password_hash(psw)

    def check_psw(self, psw):
        return check_password_hash(self.hashed_psw, psw)
