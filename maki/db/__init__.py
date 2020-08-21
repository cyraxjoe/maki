from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config
from maki.db import models

__all__ = ["models", "session", "ses"]

ses = session = scoped_session(sessionmaker())


def load_engine(config):
    engine = engine_from_config(config, prefix="")
    session.configure(bind=engine)
