from maki.utils import log
from maki import db


def update_model(model, fields, dmapper=(lambda x: x)):
    """Update the model `model` with the content of the dictionary `fields`.
    Use `dmapper` to fetch the real value from another mapper object.
    """
    if model:
        try:
            for k, v in fields.items():
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


def get_categories(locale=None, only_with_public_posts=True):
    C = db.models.Category
    P = db.models.Post
    query = db.ses.query(C.name, C.slug)
    if only_with_public_posts:
        query = (query.outerjoin(P)
                 .filter(P.public==True)
                 .group_by(C.name, C.slug))
    if locale is None or locale.showall:
        return query
    else:
        return query.filter_by(lang=locale.lang)


def clean_empty_metainfo():
    for Model in (db.models.Tag, db.models.Category):
        for elem in db.ses.query(Model):
            if not elem.endure and not elem.posts: # no post is using this.
                db.ses.delete(elem)
    db.ses.commit()


def get_user_ha1(realm, username):
    # realm is not used the stored hash already used it.
    user = db.ses.query(db.models.User).filter_by(name=username).scalar()
    if user is not None:
        return user.ha1
