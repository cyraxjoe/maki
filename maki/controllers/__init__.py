import maki.scaffold
import maki.views
from maki.controllers.post import Posts
from maki.controllers.lang import Lang
from maki.controllers.feed import Feed

__all__ = ['Posts', 'Lang', 'Feed']


class Root(maki.scaffold.Controller):
    __views__ = (maki.views.frontpage.HTML, )
    posts = Posts()
    lang = Lang()
    feed = Feed()

    def public_posts(self, page=1):
        return self.posts.public_posts(page)
