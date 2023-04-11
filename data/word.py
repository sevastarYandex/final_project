from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm, Column, Integer, String, ForeignKey, Boolean


class Word(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'word'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    word = Column(String, nullable=False)
    tr_list = Column(String, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    is_pb = Column(Boolean, nullable=False)
    user = orm.relationship('User')

    def __repr__(self):
        return f'Word(id={self.id}, word="{self.word}")'
