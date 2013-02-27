import maki.scaffold
import maki.views
from maki.controllers.login import Login
from maki.controllers.post import Post
from maki.controllers.lang import Lang
from maki.controllers.feed import Feed

__all__ = ['Login', 'Post', 'Lang', 'Feed']


class Root(maki.scaffold.Controller):
    __views__ = (maki.views.frontpage.HTML,)
    post = Post()
    login = Login()
    lang = Lang()
    feed = Feed()


    def public_posts(self, page=1):
        return self.post.public_posts(page)
