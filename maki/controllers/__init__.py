import maki.scaffold
import maki.views
from maki import db
from maki.controllers.login import Login
from maki.controllers.post import Post

__all__ = ['Login', 'Post']

class Root(maki.scaffold.Controller):
    __views__ = (maki.views.frontpage.HTML,)
    post = Post()
    login = Login()

    def get_posts(self, limit=8):
        return db.ses.query(db.models.Post).limit(limit)

