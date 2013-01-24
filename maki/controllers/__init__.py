import cherrypy

import maki.scaffold
import maki.views
from maki import db
from maki.controllers.login import Login
from maki.controllers.post import Post
from maki.controllers.lang import Lang

__all__ = ['Login', 'Post', 'Lang']

class Root(maki.scaffold.Controller):
    __views__ = (maki.views.frontpage.HTML,)
    post = Post()
    login = Login()
    lang = Lang()

    def get_posts(self, limit=8):
        locale = cherrypy.response.i18n
        posts = db.ses.query(db.models.Post).filter_by(public=True)
        if not locale.showall:
            posts = posts.filter_by(lang=locale.lang)
        return posts.limit(limit)

