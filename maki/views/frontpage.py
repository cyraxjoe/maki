import cherrypy
from cherrypy import tools

import maki.scaffold
from maki.db import utils as dbutils

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="frontpage.mako")
    def index(self,  page='1'):
        if page.isdigit():
            page = int(page)
        else:
            page = 1
        posts = self.ctrl.get_posts(page)
        pages = dbutils.public_posts_pages(posts)
        return {'posts': posts,
                'currpage': page,
                'pages': pages}


