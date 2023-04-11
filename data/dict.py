from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm, Column, Integer, String, Boolean, ForeignKey


class Dict(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dict'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    wd_ids = Column(String, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    is_pb = Column(Boolean, nullable=False)
    user = orm.relationship('User')

    def __repr__(self):
        return f'Dictionary(id={self.id}, title="{self.title}")'
