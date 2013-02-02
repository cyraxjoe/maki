import math

import maki.scaffold
import maki.views

from maki.db import utils as dbutils
from maki.constants import POSTS_PER_PAGE
from maki.controllers.login import Login
from maki.controllers.post import Post
from maki.controllers.lang import Lang

__all__ = ['Login', 'Post', 'Lang']

class Root(maki.scaffold.Controller):
    __views__ = (maki.views.frontpage.HTML,)
    post = Post()
    login = Login()
    lang = Lang()


    def get_posts(self, page=1, limit=POSTS_PER_PAGE):
        offset = (page - 1) * limit
        posts = dbutils.public_posts_query()
        return posts.offset(offset).limit(limit)

