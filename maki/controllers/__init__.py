import maki.scaffold
import maki.views
from maki.controllers.post import Post, Posts
from maki.controllers.lang import Lang
from maki.controllers.feed import Feed

__all__ = ['Post', 'Lang', 'Feed']


class Root(maki.scaffold.Controller):
    __views__ = (maki.views.frontpage.HTML, )
    post = Post()
    posts = Posts()
    lang = Lang()
    feed = Feed()

    def public_posts(self, page=1):
        return self.post.public_posts(page)
