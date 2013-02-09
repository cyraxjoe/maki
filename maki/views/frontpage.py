import cherrypy
from cherrypy import tools

import maki.scaffold

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="frontpage.mako")
    def index(self,  page='1'):
        page, pages, posts = self.ctrl.public_posts(page)
        return {'posts': posts,
                'currpage': page,
                'pages': pages}


