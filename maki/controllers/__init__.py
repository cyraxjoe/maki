import maki.scaffold
import maki.views
from maki import db
from maki.controllers.login import Login
from maki.controllers.post import Post
from maki.controllers.category import Category

__all__ = ['Login', 'Post', 'Category']

class Root(maki.scaffold.Controller):
    __views__ = (maki.views.frontpage.HTML,)
    post = Post()
    login = Login()
    category = Category()

    def get_posts(self, limit=8):
        return db.ses.query(db.models.Post).limit(limit)

