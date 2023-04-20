"""py-file with the mechanism of the db-table 'dict'"""


from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm, Column, Integer, String, Boolean, ForeignKey


class Dict(SqlAlchemyBase, SerializerMixin):
    """class of the table 'dict'
    contains next fields:
    id - unique key integer
    title - string, must be unique for each user-host
    desc - string, description of the dictionary
    wd_ids - string, ids of the words in the dictionary, format is 'id1, id2, ..., idk'
    user_id - id of the user-host
    is_pb - bool, is public
    user - host"""
    __tablename__ = 'dict'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
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
