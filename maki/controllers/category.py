import maki.scaffold
import maki.views
from maki import db

class Category(maki.scaffold.Controller):
    __views__ = (maki.views.category.HTML,)

    def get_posts(self, category):
        return db.ses.query(db.models.Post).filter_by(category=category)

    def get_category_by_slug(self, slug):
        return db.ses.query(db.models.Category).filter_by(slug=slug).scalar()
