import cherrypy
from cherrypy import tools

import maki.scaffold
import maki.feeds
from maki.utils import redirect_if_kwargs

class HTML(maki.scaffold.View):

    @cherrypy.expose
    @tools.mako(filename="frontpage.mako")
    def index(self,  page='1', **kwargs):
        redirect_if_kwargs(kwargs, '/', 'page')
        page, pages, posts = self.ctrl.public_posts(page)
        feed_url, feed_title = maki.feeds.url_and_title()
        return {'posts': posts,
                'currpage': page,
                'pages': pages,
                'feed_url': feed_url,
                'feed_title': feed_title}

    @cherrypy.expose
    def post(self, slug):
        """
        Temporal method remove in around six months.
        """
        raise cherrypy.HTTPRedirect('/posts/{}'.format(slug), 301)
