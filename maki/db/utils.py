from maki.utils import log
from maki import db


def update_model(model, fields, dmapper=(lambda x: x)):
    """Update the model `model` with the content of the dictionary `fields`.
    Use `dmapper` to fetch the real value from another mapper object.
    """
    if model:
        try:
            for k, v in fields.items():
                log((k, v))
                setattr(model, k, dmapper(v))
        except Exception:
            log('Error at k=%s and v=%s' % (k, v))
            raise 
        return True
    else:
        return False


def precautious_commit(dbs, errorm='Unable to commit the changes.'):
    """Commit the db.Session handling  any unexpected error.

    This is meant to be used on the form handling, makes use
    of the helper functions `put_mesages` to notify to add
    the errors.

    Return the error messages or None, en case of no error.
    """
    try:
        dbs.commit()
    except Exception as error:
        log(errorm, tb=True)
        emsg = '%s: %s' % (errorm, error.args[0])
        log(emsg)
        return emsg
    else:
        return None


def get_categories():
    return db.ses.query(db.models.Category).all()


