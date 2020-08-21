import sys

from cherrypy.lib import reprconf

from maki import db


def _simple_add(dbs, Model, elements):
    emodels = [Model(**element) for element in elements]
    dbs.add_all(emodels)
    return emodels


def default_post_formats(dbs):
    frmts = [
        {"name": "rst"},
    ]
    return _simple_add(dbs, db.models.PostFormat, frmts)


def default_users(dbs):
    user = {
        "name": "joe",
        "vname": "Joel Rivera",
        "email": "rivera@joel.mx",
        "active": True,
    }
    usermod = db.models.User(**user)
    usermod.ha1 = "samplepasswd"
    dbs.add(usermod)
    return usermod


def default_languages(dbs):
    langs = [{"name": "Español", "code": "es"}, {"name": "English", "code": "en"}]
    return _simple_add(dbs, db.models.Language, langs)


def load_all():
    default_languages(db.ses)
    default_post_formats(db.ses)
    default_users(db.ses)
    db.ses.commit()


if __name__ == "__main__":
    config = reprconf.Config(sys.argv[1])
    db.load_engine(config["sqlalchemy"])
    load_all()
