import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Dictionary(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dictionary'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    word_id = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey('user.id'))
    is_public = sqlalchemy.Column(sqlalchemy.Boolean)
    user = orm.relationship('User')

    def __repr__(self):
        return f'Dictionary(id={self.id}, title="{self.title}")'
