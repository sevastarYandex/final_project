"""py-file with initing of database sessions"""

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()


__factory = None


def global_init(db_file):
    """initing database with name db_file for the first time"""
    global __factory
    if __factory:
        return
    if not db_file or not db_file.strip():
        raise Exception("it's necessary to enter the database name")
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"successfully connected to the database\n{conn_str}")
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session():
    """function for creating a new database session, returns a session"""
    global __factory
    return __factory()
