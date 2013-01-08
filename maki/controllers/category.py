from . import Controller

from maki.views.category import HTMLCategory
from maki import db

class Category(Controller):
    __views__ = (HTMLCategory,)

    def get_posts(self, category):
        return db.ses.query(db.models.Post).filter_by(category=category)

    def get_category_by_slug(self, slug):
        return db.ses.query(db.models.Category).filter_by(slug=slug).scalar()
