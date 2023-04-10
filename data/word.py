import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Word(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'word'
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    word = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tr_list = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('user.id'),
        nullable=False
    )
    is_pb = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    user = orm.relationship('User')

    def __repr__(self):
        return f'Word(id={self.id}, word="{self.word}")'
