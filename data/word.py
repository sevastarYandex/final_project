import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Word(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'word'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.String, unique=True)
    translation_list = sqlalchemy.Column(sqlalchemy.String)
    host = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey('user.id'))
    user = orm.relationship('User')

    def __repr__(self):
        return f'Word(id={self.id}, word="{self.word}")'
