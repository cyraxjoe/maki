import cherrypy
from cherrypy import tools

import maki.scaffold
import maki.feeds

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="frontpage.mako")
    def index(self,  page='1'):
        page, pages, posts = self.ctrl.public_posts(page)
        feed_url, feed_title = maki.feeds.url_and_title()
        return {'posts': posts,
                'currpage': page,
                'pages': pages,
                'feed_url': feed_url,
                'feed_title': feed_title}


