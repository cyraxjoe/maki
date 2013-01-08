from . import Controller
from .post import Post
from .login import Login
from .category import Category
from maki.views.frontpage import HTMLFrontPage
from maki import db


class Root(Controller):
    __views__ = (HTMLFrontPage,)
    post = Post()
    login = Login()
    category = Category()

    def get_posts(self, limit=8):
        return db.ses.query(db.models.Post).limit(limit)
