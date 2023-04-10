import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Dict(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dict'
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    wd_ids = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('user.id'),
        nullable=False
    )
    is_pb = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    user = orm.relationship('User')

    def __repr__(self):
        return f'Dictionary(id={self.id}, title="{self.title}")'