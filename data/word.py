import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Word(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'word'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.String)
    translation_list = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey('user.id'))
    is_public = sqlalchemy.Column(sqlalchemy.Boolean)
    user = orm.relationship('User')

    def __repr__(self):
        return f'Word(id={self.id}, word="{self.word}")'
