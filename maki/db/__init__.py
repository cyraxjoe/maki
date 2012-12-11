from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config
from maki.db import models

__all__ = ['models', 'session']

session = scoped_session(sessionmaker())

def load_engine(config):
    engine =  engine_from_config(config, prefix='')
    session.configure(bind=engine)


def with_dbs(cls):
    """Class decorator to add the self.dbs attribute to the class and
    facilitate the access to the scoped_session.
    """
    def set_dbs(self, value):
        raise RuntimeError('Unable to set reserved dbs property.')
    cls.dbs = property(lambda self: session, set_dbs)
    return cls
